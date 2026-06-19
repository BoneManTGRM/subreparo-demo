# SubReparo Immune

**SubReparo Immune** is the first practical product form of SubReparo: a downloadable cyber-immune layer for websites, repos, AI agents, and small servers.

It is not a normal antivirus replacement yet. The first version focuses on the systems Cody is most likely to build and monetize first:

- GitHub repositories
- websites and landing pages
- lead forms
- AI-agent tool configurations
- secrets and `.env` hygiene
- suspicious project changes
- prompt-injection risk patterns

## Core idea

SubReparo Immune follows a Reparodynamics loop:

```text
Detect stress -> classify fracture -> contain safely -> repair -> verify -> store scar memory
```

Traditional antivirus asks: **is this known malware?**

SubReparo Immune asks: **is this system behaving like it is compromised, exposed, or drifting away from a healthy state?**

## MVP behavior

The v0 CLI can:

1. scan a folder for common secret leaks;
2. flag risky files such as `.env`, private keys, and token-looking strings;
3. detect suspicious prompt-injection phrases in text files;
4. create local scar-memory records for findings;
5. run in safe monitor mode by default.

No destructive repairs are performed automatically.

## Quick start

```bash
cd immune
python -m subreparo_immune.cli scan .
```

Optional JSON output:

```bash
python -m subreparo_immune.cli scan . --json
```

Write findings into scar memory:

```bash
python -m subreparo_immune.cli scan . --write-scars
```

Show scar memory:

```bash
python -m subreparo_immune.cli scars
```

## Safety rules

SubReparo Immune must never behave like malware. It does not hide itself, spread itself, exfiltrate files, attack other systems, or delete important data without explicit approval.

The first rule is:

> Read broadly. Detect carefully. Contain safely. Repair only with permission unless the repair is clearly low-risk.

## Roadmap

### v0.1 CLI

- local scanner
- scar-memory log
- secret leak detection
- prompt-injection pattern detection
- JSON report output

### v0.2 Website/server guard

- website uptime check
- file integrity baseline
- form-abuse detector
- safe rollback preparation

### v0.3 AI shield

- AI-agent tool permission monitor
- prompt-injection quarantine layer
- unsafe tool-call blocker

### v0.4 SubReparo ledger integration

- submit verified repair events to a private/local SubReparo ledger
- hash private evidence instead of exposing sensitive logs

## Project status

Experimental scaffold. Not production security software yet.
