from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import Finding


def stable_json_hash(data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def finding_hash(finding: Finding) -> str:
    data = finding.to_dict()
    data.pop("evidence_preview", None)
    return stable_json_hash(data)


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
