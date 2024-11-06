from typing import Any, Dict, List, Mapping

from ..exceptions import ParserError
from ..payloads.inputs import JsonFieldDefinition
from ..payloads.transformations import (
    TransformationError,
    TransformationRegistry,
    TransformationType,
)
from .base import ParserStrategy


class JsonParserStrategy(ParserStrategy[JsonFieldDefinition]):
    def __init__(self, transformations: TransformationRegistry):
        self.transformations = transformations

    def parse(
        self, log: Dict[str, Any], fields: Mapping[str, JsonFieldDefinition]
    ) -> Dict[str, Any]:
        if not isinstance(log, dict):
            raise ParserError(
                "JsonParserStrategy requires a dictionary or a valid JSON string"
            )

        matched_fields = {}
        for key, field_def in fields.items():
            if isinstance(field_def, JsonFieldDefinition):
                # Get raw value
                value = self._get_nested_value(log, field_def.path.split("."))
                if value is not None:
                    # Apply transformation before type conversion if specified
                    if field_def.transformation:
                        try:
                            value = self.transformations.apply(
                                value,
                                field_def.transformation,
                                field_def.transformation_type
                                or TransformationType.FUNCTION,
                            )
                        except TransformationError as e:
                            raise ParserError(
                                f"Transformation error for field {key}: {e!s}"
                            )
                    matched_fields[key] = value

        # Convert types after all transformations
        return self._convert_types(matched_fields, fields)

    @staticmethod
    def _get_nested_value(data: Dict[str, Any], keys: List[str]) -> Any:
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data
