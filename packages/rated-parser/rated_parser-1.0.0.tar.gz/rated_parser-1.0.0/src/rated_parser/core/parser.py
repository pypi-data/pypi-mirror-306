from typing import Any, Dict, Literal, Optional, Union

from ..exceptions import ParserError, PatternError
from ..payloads.encryption import EncryptionRegistry
from ..payloads.inputs import (
    JsonLogPatternPayload,
    LogFormat,
    RawTextLogPatternPayload,
)
from ..payloads.metric_patterns import MetricPattern
from ..payloads.transformations import (
    TransformationRegistry,
    TransformationType,
)
from ..payloads.types import ParsedEntry
from ..utils.factory import create_log_parser

PatternType = Literal["log", "metric"]


class RatedParser:
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initializes the parser with separate dictionaries for log and metric patterns
        """
        self.log_patterns: Dict[int, Dict[str, Any]] = {}
        self.metric_patterns: Dict[int, Dict[str, Any]] = {}
        self.encryption = EncryptionRegistry(encryption_key)
        self.transformations = TransformationRegistry()

    def add_log_pattern(self, pattern_dict: Dict[str, Any]) -> None:
        """
        Adds a log pattern - specific to log processing with format validation
        """
        pattern: Union[RawTextLogPatternPayload, JsonLogPatternPayload]
        log_format_str = pattern_dict["log_format"].lower()

        try:
            if log_format_str == LogFormat.RAW_TEXT:
                pattern = RawTextLogPatternPayload(**pattern_dict)
            elif log_format_str == LogFormat.JSON:
                pattern = JsonLogPatternPayload(**pattern_dict)
            else:
                raise PatternError(
                    f"Invalid log format {log_format_str}, "
                    f"use 'raw_text' or 'json_dict'"
                )

            if pattern.version in self.log_patterns:
                raise PatternError(
                    f"Log pattern version {pattern.version} already exists"
                )

            self._validate_transformations(pattern.fields)

            parser = create_log_parser(pattern, transformations=self.transformations)
            self.log_patterns[pattern.version] = {
                "parser": parser,
                "fields": {field.key: field for field in pattern.fields},
            }
        except Exception as e:
            raise PatternError(f"Error adding log pattern: {e!s}")

    def add_metric_pattern(self, pattern_dict: Dict[str, Any]) -> None:
        """
        Adds a metric pattern with the new simplified format
        """
        try:
            pattern = MetricPattern(**pattern_dict)

            if pattern.version in self.metric_patterns:
                raise PatternError(
                    f"Metric pattern version {pattern.version} already exists"
                )
            self._validate_transformations(pattern.fields)
            self.metric_patterns[pattern.version] = {
                "fields": {field.key: field for field in pattern.fields},
            }
        except Exception as e:
            raise PatternError(f"Error adding metric pattern: {e!s}")

    def _validate_transformations(self, fields: list) -> None:
        """
        Validates transformations for both logs and metrics
        """
        for field in fields:
            if field.transformation:
                try:
                    if field.transformation_type == TransformationType.EXPRESSION:
                        self.transformations.validate_expression(field.transformation)
                    elif field.transformation_type == TransformationType.FUNCTION:
                        if field.transformation not in self.transformations._processors:
                            raise ValueError(
                                f"Unknown function transformation: {field.transformation}"
                            )
                except ValueError as e:
                    raise PatternError(
                        f"Invalid transformation for field {field.key}: {e!s}"
                    )

    def parse_log(self, log: Union[str, Dict[str, Any]], version: int) -> ParsedEntry:
        """
        Parses logs using the log-specific patterns
        """
        if version not in self.log_patterns:
            raise ParserError(f"Unknown log pattern version: {version}")

        pattern = self.log_patterns[version]
        parser = pattern["parser"]
        fields = pattern["fields"]

        try:
            parsed_fields = parser.parse(log, fields)
            processed_fields = self._process_sensitive_fields(parsed_fields, fields)
            return ParsedEntry(version=version, parsed_fields=processed_fields)
        except Exception as e:
            raise ParserError(f"Error parsing log: {e!s}") from e

    def parse_metric(self, metric: Dict[str, Any], version: int) -> ParsedEntry:
        """
        Parses metrics using the metric-specific patterns.
        Only processes fields that are defined in the pattern, leaves other fields unchanged.
        """
        if version not in self.metric_patterns:
            raise ParserError(f"Unknown metric pattern version: {version}")

        pattern = self.metric_patterns[version]
        fields = pattern["fields"]

        try:
            processed_fields = metric.copy()
            for field_key, field_def in fields.items():
                if field_key in metric:
                    value = metric[field_key]

                    if field_def.encryption:
                        processed_fields[field_key] = self.encryption.encrypt(
                            str(value)
                        )
                    elif field_def.hash:
                        processed_fields[field_key] = self.encryption.basic_hash(
                            str(value)
                        )

                    if field_def.transformation:
                        processed_fields[field_key] = self.transformations.apply(
                            value,
                            field_def.transformation,
                            field_def.transformation_type,
                        )
            return ParsedEntry(version=version, parsed_fields=processed_fields)
        except Exception as e:
            raise ParserError(f"Error parsing metric: {e!s}") from e

    def _process_sensitive_fields(
        self, data: Dict[str, Any], fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processes fields that require encryption or hashing
        """
        processed = data.copy()
        for field_key, field_def in fields.items():
            if field_key in processed:
                if field_def.encryption:
                    processed[field_key] = self.encryption.encrypt(
                        str(processed[field_key])
                    )
                elif field_def.hash:
                    processed[field_key] = self.encryption.basic_hash(
                        str(processed[field_key])
                    )
        return processed

    def decrypt_field(self, value: str) -> str:
        """
        Decrypt an encrypted field value
        """
        return self.encryption.decrypt(value)
