from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from .models import Source
from .validation import validate_source, DSPValidationError

PathLike = Union[str, Path]


def load_source(path: PathLike, validate: bool = True) -> Source:
    p = Path(path)
    if not p.exists():
        raise ValueError(f"DSP manifest file not found: {p}")

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"Failed to parse JSON from {p}: {exc}") from exc

    src = Source.model_validate(data)

    if validate:
        validate_source(src)

    return src


def save_source(source: Source, path: PathLike, validate: bool = True) -> None:
    if validate:
        validate_source(source)

    p = Path(path)
    try:
        p.write_text(json.dumps(source.model_dump(mode="json"), indent=2), encoding="utf-8")
    except Exception as exc:
        raise ValueError(f"Failed to write DSP manifest to {p}: {exc}") from exc
