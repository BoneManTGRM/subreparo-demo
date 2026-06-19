from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import Finding, FractureType, Severity
from .scanners import DEFAULT_EXCLUDED_DIRS

DEFAULT_INVENTORY_PATH = Path(".subreparo") / "project_inventory.json"


@dataclass(frozen=True)
class FileRecord:
    path: str
    digest: str
    size_bytes: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProjectInventory:
    created_at: str
    root: str
    files: dict[str, FileRecord]

    def to_dict(self) -> dict[str, Any]:
        return {
            "created_at": self.created_at,
            "root": self.root,
            "files": {path: record.to_dict() for path, record in self.files.items()},
        }


def content_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_project_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in DEFAULT_EXCLUDED_DIRS or part == ".subreparo" for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def create_inventory(root: Path, inventory_path: Path = DEFAULT_INVENTORY_PATH) -> ProjectInventory:
    root = root.resolve()
    records: dict[str, FileRecord] = {}
    for path in iter_project_files(root):
        relative = str(path.relative_to(root))
        records[relative] = FileRecord(
            path=relative,
            digest=content_digest(path),
            size_bytes=path.stat().st_size,
        )

    inventory = ProjectInventory(
        created_at=datetime.now(timezone.utc).isoformat(),
        root=str(root),
        files=records,
    )
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    inventory_path.write_text(json.dumps(inventory.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return inventory


def load_inventory(inventory_path: Path = DEFAULT_INVENTORY_PATH) -> ProjectInventory | None:
    if not inventory_path.exists():
        return None
    data = json.loads(inventory_path.read_text(encoding="utf-8"))
    return ProjectInventory(
        created_at=data["created_at"],
        root=data["root"],
        files={path: FileRecord(**record) for path, record in data.get("files", {}).items()},
    )


def compare_inventory(root: Path, inventory_path: Path = DEFAULT_INVENTORY_PATH) -> list[Finding]:
    inventory = load_inventory(inventory_path)
    if inventory is None:
        return [
            Finding(
                fracture_type=FractureType.BASELINE_MISSING,
                severity=Severity.LOW,
                path=str(inventory_path),
                line=None,
                signal="No project inventory exists yet.",
                recommendation="Run `subreparo-immune inventory create .` after reviewing the project.",
            )
        ]

    root = root.resolve()
    current_records: dict[str, FileRecord] = {}
    for path in iter_project_files(root):
        relative = str(path.relative_to(root))
        current_records[relative] = FileRecord(
            path=relative,
            digest=content_digest(path),
            size_bytes=path.stat().st_size,
        )

    findings: list[Finding] = []
    inventory_paths = set(inventory.files)
    current_paths = set(current_records)

    for added in sorted(current_paths - inventory_paths):
        findings.append(
            Finding(
                fracture_type=FractureType.FILE_ADDED,
                severity=Severity.LOW,
                path=added,
                line=None,
                signal="File exists now but was not in the saved project inventory.",
                recommendation="Review the new file. If expected, save a new inventory after review.",
                evidence_preview=current_records[added].digest,
            )
        )

    for removed in sorted(inventory_paths - current_paths):
        findings.append(
            Finding(
                fracture_type=FractureType.FILE_REMOVED,
                severity=Severity.MEDIUM,
                path=removed,
                line=None,
                signal="File existed in the saved project inventory but is now missing.",
                recommendation="Confirm whether the removal was intended. Restore it or save a new inventory after review.",
                evidence_preview=inventory.files[removed].digest,
            )
        )

    for common in sorted(inventory_paths & current_paths):
        old = inventory.files[common]
        new = current_records[common]
        if old.digest != new.digest:
            findings.append(
                Finding(
                    fracture_type=FractureType.FILE_CHANGED,
                    severity=Severity.MEDIUM,
                    path=common,
                    line=None,
                    signal="File content differs from the saved project inventory.",
                    recommendation="Review the change. If expected, save a new inventory after review.",
                    evidence_preview=f"old={old.digest} new={new.digest}",
                )
            )

    return findings
