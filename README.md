# SubReparo Immune

SubReparo Immune is a project repair-memory tool.

It helps check project folders for risky configuration patterns, records findings, and turns those findings into scar-memory rules so future projects can be built more carefully.

## Core loop

```text
Detect stress -> classify fracture -> prepare repair -> verify -> store scar memory
```

## Current implementation

The first implementation lives in `immune/`.

It includes a Python CLI with two commands:

```bash
cd immune
python -m subreparo_immune.cli scan .
python -m subreparo_immune.cli scars
```

## Product direction

- v0.1: local project scanner and scar memory
- v0.2: website and repo health checks
- v0.3: AI-agent boundary checks
- v0.4: local SubReparo repair ledger
- v1.0: downloadable app and server agent

## Principle

SubReparo Immune is for systems the user owns or is authorized to maintain.

It should read carefully, repair cautiously, verify changes, and remember lessons.
