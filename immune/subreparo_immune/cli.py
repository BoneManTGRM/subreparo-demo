from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .ledger import init_ledger, insert_findings, list_events, update_event_status
from .models import Finding, Severity
from .scar_memory import append_scars, read_scars
from .scanners import scan_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-immune",
        description="SubReparo Immune: adaptive repair-memory scanner for repos, websites, and AI-agent projects.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a path for repair-memory stress signals.")
    scan_parser.add_argument("path", nargs="?", default=".", help="Path to scan. Defaults to current directory.")
    scan_parser.add_argument("--json", action="store_true", help="Output findings as JSON.")
    scan_parser.add_argument("--write-scars", action="store_true", help="Append findings to local scar memory JSONL.")
    scan_parser.add_argument("--write-ledger", action="store_true", help="Append findings to the local SQLite repair ledger.")
    scan_parser.add_argument("--fail-on", choices=[s.value for s in Severity], default=None, help="Exit with status 2 when findings at or above this severity are detected.")

    subparsers.add_parser("scars", help="Show local scar memory records.")

    ledger_parser = subparsers.add_parser("ledger", help="Manage local repair ledger records.")
    ledger_subparsers = ledger_parser.add_subparsers(dest="ledger_command", required=True)

    ledger_subparsers.add_parser("init", help="Initialize the local repair ledger.")

    list_parser = ledger_subparsers.add_parser("list", help="List repair ledger records.")
    list_parser.add_argument("--status", choices=["pending", "repaired", "verified", "rejected"], default=None)
    list_parser.add_argument("--limit", type=int, default=50)
    list_parser.add_argument("--json", action="store_true")

    update_parser = ledger_subparsers.add_parser("status", help="Update a repair ledger record status.")
    update_parser.add_argument("event_id", type=int)
    update_parser.add_argument("status", choices=["pending", "repaired", "verified", "rejected"])
    update_parser.add_argument("--note", default=None)

    return parser


def severity_rank(severity: Severity) -> int:
    order = {
        Severity.INFO: 0,
        Severity.LOW: 1,
        Severity.MEDIUM: 2,
        Severity.HIGH: 3,
        Severity.CRITICAL: 4,
    }
    return order[severity]


def print_text_findings(findings: list[Finding]) -> None:
    if not findings:
        print("SubReparo Immune: no stress signals detected.")
        return

    print(f"SubReparo Immune: {len(findings)} stress signal(s) detected.\n")
    for finding in findings:
        location = finding.path if finding.line is None else f"{finding.path}:{finding.line}"
        print(f"[{finding.severity.value.upper()}] {finding.fracture_type.value} at {location}")
        print(f"  Signal: {finding.signal}")
        if finding.evidence_preview:
            print(f"  Evidence: {finding.evidence_preview}")
        print(f"  Repair: {finding.recommendation}\n")


def command_scan(args: argparse.Namespace) -> int:
    root = Path(args.path)
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        return 1

    findings = scan_path(root)

    if args.json:
        print(json.dumps([finding.to_dict() for finding in findings], indent=2, sort_keys=True))
    else:
        print_text_findings(findings)

    if args.write_scars and findings:
        written = append_scars(findings)
        print(f"SubReparo Immune: wrote {written} scar-memory record(s).")

    if args.write_ledger and findings:
        written = insert_findings(findings)
        print(f"SubReparo Immune: wrote {written} repair-ledger record(s).")

    if args.fail_on:
        threshold = Severity(args.fail_on)
        if any(severity_rank(f.severity) >= severity_rank(threshold) for f in findings):
            return 2

    return 0


def command_scars() -> int:
    scars = read_scars()
    if not scars:
        print("SubReparo Immune: no scar memory records found.")
        return 0
    print(json.dumps(scars, indent=2, sort_keys=True))
    return 0


def print_ledger_events(events: list) -> None:
    if not events:
        print("SubReparo Immune: no repair-ledger records found.")
        return

    for event in events:
        location = event.source_path if event.line is None else f"{event.source_path}:{event.line}"
        print(f"#{event.id} [{event.status}] {event.severity.upper()} {event.fracture_type} at {location}")
        print(f"  Signal: {event.signal}")
        print(f"  Repair: {event.recommendation}")
        print(f"  Evidence hash: {event.evidence_hash}")
        if event.verification_note:
            print(f"  Note: {event.verification_note}")
        print()


def command_ledger(args: argparse.Namespace) -> int:
    if args.ledger_command == "init":
        init_ledger()
        print("SubReparo Immune: local repair ledger initialized.")
        return 0

    if args.ledger_command == "list":
        events = list_events(status=args.status, limit=args.limit)
        if args.json:
            print(json.dumps([event.to_dict() for event in events], indent=2, sort_keys=True))
        else:
            print_ledger_events(events)
        return 0

    if args.ledger_command == "status":
        updated = update_event_status(args.event_id, args.status, args.note)
        if not updated:
            print(f"SubReparo Immune: no ledger record found for id {args.event_id}.", file=sys.stderr)
            return 1
        print(f"SubReparo Immune: ledger record {args.event_id} marked {args.status}.")
        return 0

    return 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        return command_scan(args)
    if args.command == "scars":
        return command_scars()
    if args.command == "ledger":
        return command_ledger(args)

    parser.error(f"Unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
