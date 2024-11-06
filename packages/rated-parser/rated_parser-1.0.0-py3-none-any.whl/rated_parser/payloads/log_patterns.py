from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, field_validator

from .transformations import TransformationType


class FieldType(str, Enum):
    TIMESTAMP = "timestamp"
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"


class LogFormat(str, Enum):
    RAW_TEXT = "raw_text"
    JSON = "json_dict"


class LogFieldDefinition(BaseModel):
    key: str
    field_type: FieldType
    format: Optional[str] = None
    encryption: Optional[bool] = False
    hash: Optional[bool] = False
    transformation: Optional[str] = None
    transformation_type: Optional[TransformationType] = None

    @field_validator("format")
    def validate_format(cls, v, info):
        field_type = info.data.get("field_type")
        if field_type == FieldType.TIMESTAMP and not v:
            raise ValueError("Format is required for timestamp fields")
        return v

    @field_validator("encryption", "hash")
    def validate_sensitive_fields(cls, v, info):
        field_type = info.data.get("field_type")
        if field_type == FieldType.TIMESTAMP and v is True:
            raise ValueError(f"Timestamp fields cannot be {info.field_name}")
        return v

    @field_validator("transformation_type")
    def validate_transformation_type(cls, v, info):
        transformation = info.data.get("transformation")
        if transformation and not v:
            return (
                TransformationType.FUNCTION
                if transformation.isidentifier()
                else TransformationType.EXPRESSION
            )
        return v


class LogPatternBase(BaseModel):
    version: int
    log_format: LogFormat


class RawTextLogPattern(LogPatternBase):
    log_example: str
    fields: List[LogFieldDefinition]


class JsonLogPattern(LogPatternBase):
    fields: List[LogFieldDefinition]
