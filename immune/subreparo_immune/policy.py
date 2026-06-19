from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ProductPolicy:
    monitor_only: bool = True
    write_ledger_by_default: bool = False
    keep_private_content_local: bool = True
    require_approval_for_repairs: bool = True
    max_watch_interval_seconds: int = 3600
    min_watch_interval_seconds: int = 10

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DEFAULT_POLICY = ProductPolicy()
DEFAULT_POLICY_PATH = Path(".subreparo") / "policy.json"


def write_default_policy(path: Path = DEFAULT_POLICY_PATH) -> None:
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(DEFAULT_POLICY.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
