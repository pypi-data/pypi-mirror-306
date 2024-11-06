import ast
from enum import Enum
from typing import Any, Callable, ClassVar, Dict, Set

from simpleeval import InvalidExpression, simple_eval  # type: ignore

from ..core.constants.http import HTTPStatus


class TransformationType(str, Enum):
    FUNCTION = "function"
    EXPRESSION = "expression"


class TransformationError(Exception):
    """Custom error for transformation failures"""

    def __init__(self, message: str, expression: str):
        self.expression = expression
        super().__init__(message)


class TransformationRegistry:
    # Safe operations for log parsing
    ALLOWED_OPERATORS: ClassVar[Set[type]] = {
        ast.Add,  # +
        ast.Sub,  # -
        ast.Mult,  # *
        ast.Div,  # /
        ast.Call,  # Function calls
        ast.USub,  # Negative numbers
        ast.Compare,  # Comparisons
        ast.Lt,  #
        ast.LtE,  # <=
        ast.Gt,  # >
        ast.GtE,  # >=
        ast.Eq,  # ==
        ast.NotEq,  # !=
        ast.Mod,  # %
        ast.Attribute,  # Allow attribute access
    }

    ALLOWED_FUNCTIONS: ClassVar[Set[str]] = {
        # Type conversions
        "float",
        "int",
        "str",
        "bool",
        # String operations
        "len",
        "abs",
        # Math operations
        "round",
        "min",
        "max",
    }

    # Safe string methods
    ALLOWED_ATTRIBUTES: ClassVar[Set[str]] = {
        # String cleaning
        "strip",
        "lstrip",
        "rstrip",
        # Case conversion
        "upper",
        "lower",
        "title",
        "capitalize",
        # String operations
        "replace",
        "split",
        "join",
        # String checks
        "startswith",
        "endswith",
        "isdigit",
        "isalpha",
        "isalnum",
    }

    def __init__(self):
        self._processors: Dict[str, Callable] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        defaults = {
            # Duration conversions
            "duration_to_ms": lambda x: float(str(x).rstrip("s")) * 1000,
            "duration_to_seconds": lambda x: float(str(x).rstrip("s")),
            # Status code helpers
            "is_success": lambda x: HTTPStatus.MIN_SUCCESS
            <= int(x)
            < HTTPStatus.MAX_SUCCESS,
            "is_error": lambda x: int(x) >= HTTPStatus.MIN_ERROR,
            "status_class": lambda x: f"{int(int(x) / 100)}xx",
            # String cleaning
            "normalize_whitespace": lambda x: " ".join(str(x).split()),
            "strip_quotes": lambda x: str(x).strip("\"'"),
        }
        self._processors.update(defaults)

    def register(self, name: str, func: Callable) -> None:
        if name in self._processors:
            raise ValueError(f"Transformation '{name}' already registered")
        self._processors[name] = func

    def validate_expression(self, expression: str) -> bool:  # noqa: C901
        try:
            tree = ast.parse(expression, mode="eval")

            for node in ast.walk(tree):
                # Check operators
                if (
                    isinstance(node, ast.operator)
                    and type(node) not in self.ALLOWED_OPERATORS
                ):
                    raise ValueError(f"Operation {type(node).__name__} is not allowed")

                # Check function calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id not in self.ALLOWED_FUNCTIONS:
                            raise ValueError(f"Function '{node.func.id}' not allowed")
                    elif not isinstance(node.func, ast.Attribute):
                        raise ValueError("Only simple function calls are allowed")

                # Check attribute access
                if isinstance(node, ast.Attribute):
                    if node.attr.startswith("__"):
                        raise ValueError(
                            "Access to double underscore attributes not allowed"
                        )
                    if node.attr not in self.ALLOWED_ATTRIBUTES:
                        raise ValueError(f"Attribute '{node.attr}' not allowed")

                # Prevent complex operations
                if isinstance(
                    node,
                    (
                        ast.List,
                        ast.Dict,
                        ast.Set,
                        ast.ListComp,
                        ast.DictComp,
                        ast.SetComp,
                    ),
                ):
                    raise ValueError("List/dict/set operations not allowed")

            return True
        except SyntaxError as e:
            raise ValueError(f"Invalid expression syntax: {e!s}")

    def apply(
        self, value: Any, transformation: str, transform_type: TransformationType
    ) -> Any:
        try:
            if transform_type == TransformationType.FUNCTION:
                processor = self._processors.get(transformation)
                if not processor:
                    raise ValueError(
                        f"Unknown transformation function: {transformation}"
                    )
                return processor(value)
            else:  # EXPRESSION
                self.validate_expression(transformation)
                return simple_eval(transformation, names={"value": value})
        except (ValueError, InvalidExpression) as e:
            raise TransformationError(str(e), transformation)
        except Exception as e:
            raise TransformationError(f"Transformation failed: {e!s}", transformation)
