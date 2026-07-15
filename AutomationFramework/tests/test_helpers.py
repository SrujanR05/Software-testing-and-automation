from __future__ import annotations

from pathlib import Path


def load_json_fixture(path: str | Path) -> dict:
    import json

    return json.loads(Path(path).read_text(encoding="utf-8"))
