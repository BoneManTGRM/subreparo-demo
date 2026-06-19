from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .evidence import finding_hash
from .models import Finding
from .scar_memory import scar_from_finding

DEFAULT_LEDGER_PATH = Path(".subreparo") / "repair_ledger.sqlite3"
SCHEMA_VERSION = 1


@dataclass(frozen=True)
class LedgerEvent:
    id: int
    created_at: str
    status: str
    fracture_type: str
    severity: str
    source_path: str
    line: int | None
    signal: str
    recommendation: str
    evidence_hash: str
    verification_note: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "status": self.status,
            "fracture_type": self.fracture_type,
            "severity": self.severity,
            "source_path": self.source_path,
            "line": self.line,
            "signal": self.signal,
            "recommendation": self.recommendation,
            "evidence_hash": self.evidence_hash,
            "verification_note": self.verification_note,
        }


def connect(path: Path = DEFAULT_LEDGER_PATH) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def init_ledger(path: Path = DEFAULT_LEDGER_PATH) -> None:
    with connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS repair_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                status TEXT NOT NULL,
                fracture_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                source_path TEXT NOT NULL,
                line INTEGER,
                signal TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                evidence_preview TEXT,
                evidence_hash TEXT NOT NULL,
                scar_json TEXT NOT NULL,
                verification_note TEXT
            )
            """
        )
        connection.execute(
            "INSERT OR REPLACE INTO metadata(key, value) VALUES(?, ?)",
            ("schema_version", str(SCHEMA_VERSION)),
        )


def insert_findings(findings: list[Finding], path: Path = DEFAULT_LEDGER_PATH) -> int:
    init_ledger(path)
    now = datetime.now(timezone.utc).isoformat()
    inserted = 0
    with connect(path) as connection:
        for finding in findings:
            scar = scar_from_finding(finding)
            connection.execute(
                """
                INSERT INTO repair_events(
                    created_at,
                    updated_at,
                    status,
                    fracture_type,
                    severity,
                    source_path,
                    line,
                    signal,
                    recommendation,
                    evidence_preview,
                    evidence_hash,
                    scar_json,
                    verification_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    now,
                    now,
                    "pending",
                    finding.fracture_type.value,
                    finding.severity.value,
                    finding.path,
                    finding.line,
                    finding.signal,
                    finding.recommendation,
                    finding.evidence_preview,
                    finding_hash(finding),
                    json.dumps(scar.to_dict(), sort_keys=True),
                    None,
                ),
            )
            inserted += 1
    return inserted


def list_events(status: str | None = None, limit: int = 50, path: Path = DEFAULT_LEDGER_PATH) -> list[LedgerEvent]:
    init_ledger(path)
    query = "SELECT * FROM repair_events"
    params: list[Any] = []
    if status:
        query += " WHERE status = ?"
        params.append(status)
    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    with connect(path) as connection:
        rows = connection.execute(query, params).fetchall()

    return [row_to_event(row) for row in rows]


def update_event_status(event_id: int, status: str, note: str | None = None, path: Path = DEFAULT_LEDGER_PATH) -> bool:
    if status not in {"pending", "verified", "rejected", "repaired"}:
        raise ValueError("status must be one of: pending, repaired, verified, rejected")

    init_ledger(path)
    now = datetime.now(timezone.utc).isoformat()
    with connect(path) as connection:
        cursor = connection.execute(
            """
            UPDATE repair_events
            SET status = ?, verification_note = ?, updated_at = ?
            WHERE id = ?
            """,
            (status, note, now, event_id),
        )
        return cursor.rowcount > 0


def row_to_event(row: sqlite3.Row) -> LedgerEvent:
    return LedgerEvent(
        id=int(row["id"]),
        created_at=str(row["created_at"]),
        status=str(row["status"]),
        fracture_type=str(row["fracture_type"]),
        severity=str(row["severity"]),
        source_path=str(row["source_path"]),
        line=row["line"],
        signal=str(row["signal"]),
        recommendation=str(row["recommendation"]),
        evidence_hash=str(row["evidence_hash"]),
        verification_note=row["verification_note"],
    )
