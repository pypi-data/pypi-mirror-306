from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, Generic, Mapping, Optional, TypeVar

from ..exceptions import ParserError
from ..payloads.inputs import FieldDefinition, FieldType

T = TypeVar("T", bound=FieldDefinition)


class ParserStrategy(Generic[T], ABC):
    @abstractmethod
    def parse(self, log: Any, fields: Dict[str, T]) -> Dict[str, Any]:
        pass

    @staticmethod
    def _parse_timestamp(value: str, date_format: Optional[str]) -> datetime:
        if date_format is None:
            raise ValueError("date_format must be provided")

        dt = datetime.strptime(value, date_format)
        if date_format.endswith("%z") or date_format.endswith("%Z"):
            # datetime object already has timezone info
            return dt
        elif value.endswith("Z"):
            # if value ends with Z, it's UTC
            return dt.replace(tzinfo=timezone.utc)
        else:
            # Otherwise, assume UTC
            return dt.replace(tzinfo=timezone.utc)

    def _convert_types(
        self, matched_fields: Dict[str, Any], fields: Mapping[str, FieldDefinition]
    ) -> Dict[str, Any]:
        for key, value in matched_fields.items():
            field_def = fields.get(key)
            if field_def:
                try:
                    if field_def.field_type == FieldType.INTEGER:
                        matched_fields[key] = int(value)
                    elif field_def.field_type == FieldType.FLOAT:
                        matched_fields[key] = float(value)
                    elif field_def.field_type == FieldType.TIMESTAMP:
                        matched_fields[key] = self._parse_timestamp(
                            value, field_def.format
                        )
                except ValueError as e:
                    raise ParserError(f"Error converting field '{key}': {e!s}")
        return matched_fields
