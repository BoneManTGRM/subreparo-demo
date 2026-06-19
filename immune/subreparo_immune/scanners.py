from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from .models import Finding, FractureType, Severity


DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "target",
    "__pycache__",
    ".venv",
    "venv",
}

SENSITIVE_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".npmrc",
    "id_rsa",
    "id_ed25519",
    "wallet.dat",
    "secrets.json",
}

SECRET_PATTERNS: list[tuple[str, re.Pattern[str], Severity]] = [
    ("OpenAI-style API key", re.compile(r"sk-[A-Za-z0-9_\-]{20,}"), Severity.CRITICAL),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"), Severity.CRITICAL),
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}"), Severity.CRITICAL),
    ("Private key block", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"), Severity.CRITICAL),
    ("Generic assignment secret", re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{8,}['\"]"), Severity.HIGH),
]

PROMPT_INJECTION_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("ignore previous instructions", re.compile(r"(?i)ignore (all )?(previous|prior|above) instructions")),
    ("reveal system prompt", re.compile(r"(?i)(reveal|print|show).{0,40}(system prompt|developer message|hidden instructions)")),
    ("tool escalation", re.compile(r"(?i)(use|call|invoke).{0,40}(tool|function|api).{0,40}(without|bypass|ignore).{0,30}(permission|approval)")),
    ("data exfiltration instruction", re.compile(r"(?i)(send|upload|exfiltrate|copy).{0,40}(secrets|tokens|private keys|\.env)")),
]

TEXT_SUFFIXES = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".toml", ".yaml", ".yml", ".env", ".md", ".txt", ".html", ".css", ".rs", ".go", ".java", ".sh"
}


def iter_files(root: Path, excluded_dirs: set[str] | None = None) -> Iterable[Path]:
    excluded = excluded_dirs or DEFAULT_EXCLUDED_DIRS
    for path in root.rglob("*"):
        if any(part in excluded for part in path.parts):
            continue
        if path.is_file():
            yield path


def is_text_candidate(path: Path) -> bool:
    if path.name in SENSITIVE_FILENAMES:
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def read_text_safely(path: Path, max_bytes: int = 1_000_000) -> str | None:
    try:
        if path.stat().st_size > max_bytes:
            return None
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def scan_path(root: Path) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []

    for path in iter_files(root):
        relative_path = str(path.relative_to(root))

        if path.name in SENSITIVE_FILENAMES:
            findings.append(
                Finding(
                    fracture_type=FractureType.SENSITIVE_FILE,
                    severity=Severity.HIGH,
                    path=relative_path,
                    line=None,
                    signal=f"Sensitive file present: {path.name}",
                    recommendation="Do not commit this file. Replace with a safe .env.example or encrypted secret manager reference.",
                )
            )

        if not is_text_candidate(path):
            continue

        text = read_text_safely(path)
        if not text:
            continue

        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            for label, pattern, severity in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            fracture_type=FractureType.SECRET_LEAK,
                            severity=severity,
                            path=relative_path,
                            line=line_number,
                            signal=label,
                            recommendation="Remove the secret from code, rotate it if real, and store it in a secret manager or local environment file.",
                            evidence_preview=line.strip()[:160],
                        )
                    )

            for label, pattern in PROMPT_INJECTION_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            fracture_type=FractureType.PROMPT_INJECTION_RISK,
                            severity=Severity.MEDIUM,
                            path=relative_path,
                            line=line_number,
                            signal=label,
                            recommendation="Treat this content as untrusted input. It must not override system, developer, or tool-permission rules.",
                            evidence_preview=line.strip()[:160],
                        )
                    )

    return findings
