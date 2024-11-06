from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, field_validator

from ..payloads.transformations import TransformationType


class FieldType(str, Enum):
    TIMESTAMP = "timestamp"
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"


class LogFormat(str, Enum):
    RAW_TEXT = "raw_text"
    JSON = "json_dict"


class FieldDefinition(BaseModel):
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

    @field_validator("encryption")
    def validate_encryption_for_timestamp(cls, v, info):
        field_type = info.data.get("field_type")
        if field_type == FieldType.TIMESTAMP and v is True:
            raise ValueError("Timestamp fields cannot be encrypted")
        return v

    @field_validator("hash")
    def validate_hash_for_timestamp(cls, v, info):
        field_type = info.data.get("field_type")
        if field_type == FieldType.TIMESTAMP and v is True:
            raise ValueError("Timestamp fields cannot be hashed")
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


class RawTextFieldDefinition(FieldDefinition):
    value: str


class JsonFieldDefinition(FieldDefinition):
    path: str


class LogPatternPayload(BaseModel):
    version: int
    log_format: LogFormat


class RawTextLogPatternPayload(LogPatternPayload):
    log_example: str
    fields: List[RawTextFieldDefinition]


class JsonLogPatternPayload(LogPatternPayload):
    fields: List[JsonFieldDefinition]
