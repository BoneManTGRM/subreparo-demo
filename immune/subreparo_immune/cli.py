from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from .inventory import compare_inventory, create_inventory, load_inventory
from .ledger import init_ledger, insert_findings, list_events, update_event_status
from .models import Finding, Severity
from .scar_memory import append_scars, read_scars
from .scanners import scan_path
from .webcheck import check_website, website_finding


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-immune",
        description="SubReparo Immune: repair-memory scanner for repos, websites, and AI-agent projects.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a path for repair-memory stress signals.")
    scan_parser.add_argument("path", nargs="?", default=".", help="Path to scan. Defaults to current directory.")
    scan_parser.add_argument("--json", action="store_true", help="Output findings as JSON.")
    scan_parser.add_argument("--write-scars", action="store_true", help="Append findings to local scar memory JSONL.")
    scan_parser.add_argument("--write-ledger", action="store_true", help="Append findings to the local SQLite repair ledger.")
    scan_parser.add_argument("--fail-on", choices=[s.value for s in Severity], default=None, help="Exit with status 2 when findings at or above this severity are detected.")

    subparsers.add_parser("scars", help="Show local scar memory records.")

    inventory_parser = subparsers.add_parser("inventory", help="Create or compare a saved project inventory.")
    inventory_subparsers = inventory_parser.add_subparsers(dest="inventory_command", required=True)

    inventory_create = inventory_subparsers.add_parser("create", help="Save the current project inventory.")
    inventory_create.add_argument("path", nargs="?", default=".")

    inventory_check = inventory_subparsers.add_parser("check", help="Compare project files to the saved inventory.")
    inventory_check.add_argument("path", nargs="?", default=".")
    inventory_check.add_argument("--json", action="store_true")
    inventory_check.add_argument("--write-ledger", action="store_true")

    inventory_subparsers.add_parser("show", help="Show the saved project inventory metadata.")

    website_parser = subparsers.add_parser("website", help="Run a website health check.")
    website_parser.add_argument("url")
    website_parser.add_argument("--json", action="store_true")
    website_parser.add_argument("--write-ledger", action="store_true")

    watch_parser = subparsers.add_parser("watch", help="Run repeated scans for an approved project path.")
    watch_parser.add_argument("path", nargs="?", default=".")
    watch_parser.add_argument("--interval", type=int, default=60)
    watch_parser.add_argument("--once", action="store_true")
    watch_parser.add_argument("--write-ledger", action="store_true")

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


def write_outputs(findings: list[Finding], *, write_scars: bool = False, write_ledger: bool = False) -> None:
    if write_scars and findings:
        written = append_scars(findings)
        print(f"SubReparo Immune: wrote {written} scar-memory record(s).")
    if write_ledger and findings:
        written = insert_findings(findings)
        print(f"SubReparo Immune: wrote {written} repair-ledger record(s).")


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

    write_outputs(findings, write_scars=args.write_scars, write_ledger=args.write_ledger)

    if args.fail_on:
        threshold = Severity(args.fail_on)
        if any(severity_rank(f.severity) >= severity_rank(threshold) for f in findings):
            return 2

    return 0


def command_inventory(args: argparse.Namespace) -> int:
    if args.inventory_command == "create":
        inventory = create_inventory(Path(args.path))
        print(f"SubReparo Immune: saved inventory with {len(inventory.files)} file(s).")
        return 0

    if args.inventory_command == "check":
        findings = compare_inventory(Path(args.path))
        if args.json:
            print(json.dumps([finding.to_dict() for finding in findings], indent=2, sort_keys=True))
        else:
            print_text_findings(findings)
        write_outputs(findings, write_ledger=args.write_ledger)
        return 0

    if args.inventory_command == "show":
        inventory = load_inventory()
        if inventory is None:
            print("SubReparo Immune: no saved project inventory found.")
            return 1
        print(json.dumps({"created_at": inventory.created_at, "root": inventory.root, "files": len(inventory.files)}, indent=2, sort_keys=True))
        return 0

    return 1


def command_website(args: argparse.Namespace) -> int:
    result = check_website(args.url)
    finding = website_finding(result)
    payload = {"url": result.url, "ok": result.ok, "status_code": result.status_code, "message": result.message}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        status = "OK" if result.ok else "CHECK"
        print(f"SubReparo Immune: [{status}] {result.url} - {result.message}")
    findings = [finding] if finding else []
    write_outputs(findings, write_ledger=args.write_ledger)
    return 0 if result.ok else 2


def command_watch(args: argparse.Namespace) -> int:
    interval = max(10, args.interval)
    while True:
        scan_findings = scan_path(Path(args.path))
        inventory_findings = compare_inventory(Path(args.path))
        findings = scan_findings + inventory_findings
        print_text_findings(findings)
        write_outputs(findings, write_ledger=args.write_ledger)
        if args.once:
            return 0
        time.sleep(interval)


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
    if args.command == "inventory":
        return command_inventory(args)
    if args.command == "website":
        return command_website(args)
    if args.command == "watch":
        return command_watch(args)
    if args.command == "scars":
        return command_scars()
    if args.command == "ledger":
        return command_ledger(args)

    parser.error(f"Unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
