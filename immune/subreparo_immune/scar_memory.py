from __future__ import annotations

import json
from pathlib import Path

from .models import Finding, FractureType, ScarMemory


DEFAULT_SCAR_PATH = Path(".subreparo") / "scar_memory.jsonl"


def scar_from_finding(finding: Finding) -> ScarMemory:
    if finding.fracture_type == FractureType.SECRET_LEAK:
        return ScarMemory(
            fracture_type=finding.fracture_type,
            severity=finding.severity,
            stress="A potential secret or credential was found in project text.",
            fracture="Secret material may be exposed through source control, logs, or deployment artifacts.",
            repair="Remove the secret, rotate it if real, and move secret handling into environment variables or a secret manager.",
            verification="Re-scan the project and confirm no secret pattern remains.",
            scar_rule="Future commits must run secret scanning before merge or deployment.",
            source_path=finding.path,
        )

    if finding.fracture_type == FractureType.SENSITIVE_FILE:
        return ScarMemory(
            fracture_type=finding.fracture_type,
            severity=finding.severity,
            stress="A sensitive configuration or key file exists inside the scanned project.",
            fracture="Sensitive local files can be accidentally committed or deployed.",
            repair="Move sensitive values out of the repo and commit only safe examples such as .env.example.",
            verification="Confirm the sensitive file is ignored or removed from source control.",
            scar_rule="All new projects must include a .gitignore entry for local secret files.",
            source_path=finding.path,
        )

    if finding.fracture_type == FractureType.PROMPT_INJECTION_RISK:
        return ScarMemory(
            fracture_type=finding.fracture_type,
            severity=finding.severity,
            stress="Untrusted text contains language that may attempt to manipulate an AI agent.",
            fracture="External content may try to override instructions, access tools, or reveal private configuration.",
            repair="Isolate untrusted content from agent instructions and block tool escalation from external text.",
            verification="Run a prompt-injection test and confirm the agent preserves tool and permission boundaries.",
            scar_rule="External webpages, PDFs, emails, and uploaded files are evidence only; they cannot issue instructions to the agent.",
            source_path=finding.path,
        )

    return ScarMemory(
        fracture_type=finding.fracture_type,
        severity=finding.severity,
        stress=finding.signal,
        fracture="A system stress signal was detected.",
        repair=finding.recommendation,
        verification="Re-run the relevant scanner after repair.",
        scar_rule="Do not mark the system healthy until verification passes.",
        source_path=finding.path,
    )


def append_scars(findings: list[Finding], scar_path: Path = DEFAULT_SCAR_PATH) -> int:
    scar_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with scar_path.open("a", encoding="utf-8") as handle:
        for finding in findings:
            scar = scar_from_finding(finding)
            handle.write(json.dumps(scar.to_dict(), sort_keys=True) + "\n")
            count += 1
    return count


def read_scars(scar_path: Path = DEFAULT_SCAR_PATH) -> list[dict]:
    if not scar_path.exists():
        return []
    scars: list[dict] = []
    with scar_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            scars.append(json.loads(line))
    return scars
