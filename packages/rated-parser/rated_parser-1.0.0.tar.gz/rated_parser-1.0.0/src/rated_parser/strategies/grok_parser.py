from typing import Any, Dict

from pygrok import Grok  # type: ignore

from ..exceptions import ParserError
from ..payloads.inputs import RawTextFieldDefinition
from ..payloads.transformations import (
    TransformationError,
    TransformationRegistry,
    TransformationType,
)
from .base import ParserStrategy


class GrokParserStrategy(ParserStrategy[RawTextFieldDefinition]):
    def __init__(self, pattern: str, transformations: TransformationRegistry):
        self.grok = Grok(pattern)
        self.transformations = transformations

    def parse(
        self, log: str, fields: Dict[str, RawTextFieldDefinition]
    ) -> Dict[str, Any]:
        match = self.grok.match(log)
        if not match:
            raise ParserError("Failed to parse log with the given pattern")

        transformed_match = {}
        for field_key, value in match.items():
            field_def = fields.get(field_key)
            transformed_value = value
            if field_def and value is not None:
                if field_def.transformation:
                    try:
                        transformed_value = self.transformations.apply(
                            value,
                            field_def.transformation,
                            field_def.transformation_type
                            or TransformationType.FUNCTION,
                        )
                    except TransformationError as e:
                        raise ParserError(
                            f"Transformation error for field {field_key}: {e!s}"
                        )
            transformed_match[field_key] = transformed_value

        return self._convert_types(transformed_match, fields)
