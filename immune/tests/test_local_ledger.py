from pathlib import Path

from subreparo_immune.ledger import insert_findings, list_events, update_event_status
from subreparo_immune.models import Finding, FractureType, Severity


def sample_finding() -> Finding:
    return Finding(
        fracture_type=FractureType.CONFIG_RISK,
        severity=Severity.LOW,
        path="example.txt",
        line=None,
        signal="Example project check",
        recommendation="Review project setting and confirm expected state.",
    )


def test_writes_and_lists_events(tmp_path: Path) -> None:
    db_path = tmp_path / "events.sqlite3"
    inserted = insert_findings([sample_finding()], path=db_path)
    events = list_events(path=db_path)

    assert inserted == 1
    assert len(events) == 1
    assert events[0].status == "pending"
    assert events[0].evidence_hash


def test_updates_event_status(tmp_path: Path) -> None:
    db_path = tmp_path / "events.sqlite3"
    insert_findings([sample_finding()], path=db_path)
    event = list_events(path=db_path)[0]

    assert update_event_status(event.id, "verified", "check passed", path=db_path)

    updated_event = list_events(path=db_path)[0]
    assert updated_event.status == "verified"
    assert updated_event.verification_note == "check passed"
