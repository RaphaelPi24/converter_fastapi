from pathlib import Path
from typing import ClassVar, Iterable, Tuple

from pydantic import BaseModel, field_validator, model_validator


class ConversionParams(BaseModel):
    source_format: str
    target_format: str
    input_data: Path
    output_path: Path

    allowed_source: ClassVar[Iterable[str]] = []
    allowed_target: ClassVar[Iterable[str]] = []
    allowed_pairs: ClassVar[Iterable[Tuple[str, str]]] = []

    @classmethod
    @field_validator("source_format")
    def validate_source_format(cls, v):
        if v not in cls.allowed_source:
            raise ValueError(f"Конвертация из {v} не поддерживается")
        return v

    @classmethod
    @field_validator("target_format")
    def validate_target_format(cls, v):
        if v not in cls.allowed_target:
            raise ValueError(f"Конвертация в {v} не поддерживается")
        return v

    @classmethod
    @field_validator("input_data")
    def validate_input_path(cls, v):
        if not isinstance(v, Path):
            raise TypeError("input_data должен быть типом Path")
        return v

    @classmethod
    @field_validator("output_path")
    def validate_output_path(cls, v):
        if not isinstance(v, Path):
            raise TypeError("output_path должен быть типом Path")
        return v

    @model_validator(mode="after")
    def validate_pair(self):
        pair = (self.source_format, self.target_format)
        if self.allowed_pairs and pair not in self.allowed_pairs:
            raise ValueError(f"Конвертация {pair[0]} → {pair[1]} не поддерживается")
        return self
