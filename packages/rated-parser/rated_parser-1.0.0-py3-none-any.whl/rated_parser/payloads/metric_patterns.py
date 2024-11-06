from typing import List, Optional

from pydantic import BaseModel, field_validator

from .transformations import TransformationType


class MetricFieldDefinition(BaseModel):
    key: str
    encryption: Optional[bool] = False
    hash: Optional[bool] = False
    transformation: Optional[str] = None
    transformation_type: Optional[TransformationType] = None

    @field_validator("encryption", "hash")
    def validate_sensitive_fields(cls, v, info):
        if info.field_name == "encryption" and v:
            if info.data.get("hash"):
                raise ValueError("Field cannot be both encrypted and hashed")
        elif info.field_name == "hash" and v:
            if info.data.get("encryption"):
                raise ValueError("Field cannot be both encrypted and hashed")
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


class MetricPattern(BaseModel):
    version: int
    fields: List[MetricFieldDefinition]
