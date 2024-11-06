import re
from typing import List, Union

from ..exceptions import PatternError
from ..payloads.inputs import (
    FieldType,
    JsonLogPatternPayload,
    RawTextFieldDefinition,
    RawTextLogPatternPayload,
)
from ..payloads.transformations import TransformationRegistry
from ..strategies import GrokParserStrategy, JsonParserStrategy, ParserStrategy


def create_log_parser(
    pattern: Union[RawTextLogPatternPayload, JsonLogPatternPayload],
    transformations: TransformationRegistry,
) -> ParserStrategy:
    if isinstance(pattern, RawTextLogPatternPayload):
        try:
            grok_pattern = _build_grok_pattern(pattern.log_example, pattern.fields)
            return GrokParserStrategy(grok_pattern, transformations)
        except Exception as e:
            raise PatternError(f"Error creating Grok parser: {e!s}")
    elif isinstance(pattern, JsonLogPatternPayload):
        return JsonParserStrategy(transformations)
    else:
        raise PatternError("Invalid log pattern payload type")


def _build_grok_pattern(
    raw_log_example: str, fields: List[RawTextFieldDefinition]
) -> str:
    try:
        grok_pattern = re.escape(raw_log_example)

        for field in fields:
            if field.field_type == FieldType.INTEGER:
                grok_field = f"%{{INT:{field.key}}}"
            elif field.field_type == FieldType.FLOAT:
                grok_field = f"%{{NUMBER:{field.key}}}"
            else:
                grok_field = f"%{{GREEDYDATA:{field.key}}}"

            escaped_value = re.escape(field.value)
            grok_pattern = grok_pattern.replace(escaped_value, grok_field)

        print(f"Generated Grok pattern: {grok_pattern}")
        return grok_pattern
    except Exception as e:
        raise PatternError(f"Error building Grok pattern: {e!s}")
