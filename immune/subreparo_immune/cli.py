from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .models import Finding, Severity
from .scar_memory import append_scars, read_scars
from .scanners import scan_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-immune",
        description="SubReparo Immune: adaptive repair-memory scanner for repos, websites, and AI-agent projects.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a path for immune-system stress signals.")
    scan_parser.add_argument("path", nargs="?", default=".", help="Path to scan. Defaults to current directory.")
    scan_parser.add_argument("--json", action="store_true", help="Output findings as JSON.")
    scan_parser.add_argument("--write-scars", action="store_true", help="Append findings to local scar memory.")
    scan_parser.add_argument("--fail-on", choices=[s.value for s in Severity], default=None, help="Exit with status 2 when findings at or above this severity are detected.")

    subparsers.add_parser("scars", help="Show local scar memory records.")

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


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        return command_scan(args)
    if args.command == "scars":
        return command_scars()

    parser.error(f"Unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
