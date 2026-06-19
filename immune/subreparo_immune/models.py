from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FractureType(str, Enum):
    SECRET_LEAK = "secret_leak"
    PROMPT_INJECTION_RISK = "prompt_injection_risk"
    SENSITIVE_FILE = "sensitive_file"
    SUSPICIOUS_FILE = "suspicious_file"
    CONFIG_RISK = "config_risk"


@dataclass(frozen=True)
class Finding:
    fracture_type: FractureType
    severity: Severity
    path: str
    line: int | None
    signal: str
    recommendation: str
    evidence_preview: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["fracture_type"] = self.fracture_type.value
        data["severity"] = self.severity.value
        return data


@dataclass(frozen=True)
class ScarMemory:
    fracture_type: FractureType
    severity: Severity
    stress: str
    fracture: str
    repair: str
    verification: str
    scar_rule: str
    source_path: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["fracture_type"] = self.fracture_type.value
        data["severity"] = self.severity.value
        return data


def normalize_path(path: Path) -> str:
    try:
        return str(path.resolve())
    except OSError:
        return str(path)
