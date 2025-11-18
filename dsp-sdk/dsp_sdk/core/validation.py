from __future__ import annotations

import json
from importlib.resources import files

from jsonschema import validate as js_validate, ValidationError as JSONSchemaValidationError

from .models import Source


class DSPValidationError(Exception):
    """Raised when a DSP manifest fails JSON Schema validation."""


def load_core_schema() -> dict:
    schema_path = files("dsp_sdk.schemas").joinpath("dsp-1.0.json")
    return json.loads(schema_path.read_text(encoding="utf-8"))


_CORE_SCHEMA = load_core_schema()


def validate_source(source: Source) -> None:
    try:
        js_validate(instance=source.model_dump(mode="json"), schema=_CORE_SCHEMA)
    except JSONSchemaValidationError as exc:
        raise DSPValidationError(str(exc)) from exc
