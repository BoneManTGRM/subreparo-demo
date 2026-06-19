# SubReparo Immune

SubReparo Immune is a project repair-memory system for software, websites, repositories, and AI-agent projects.

It helps check project folders for risky configuration patterns, records findings, turns those findings into scar-memory rules, and stores repair events in a local ledger so future projects can be built more carefully.

## Core loop

```text
Detect stress -> classify fracture -> prepare repair -> verify -> store scar memory -> adapt
```

## Current implementation

The first implementation lives in `immune/`.

It includes a Python CLI that can:

- scan a project folder;
- print findings as text or JSON;
- write findings to scar memory;
- write findings to a local SQLite repair ledger;
- mark repair events as pending, repaired, verified, or rejected.

## Quick start

```bash
cd immune
python -m subreparo_immune.cli scan .
python -m subreparo_immune.cli scan . --json
python -m subreparo_immune.cli scan . --write-scars
python -m subreparo_immune.cli scan . --write-ledger
python -m subreparo_immune.cli ledger list
python -m subreparo_immune.cli ledger status 1 verified --note "check passed"
python -m subreparo_immune.cli scars
```

## Chain foundation

The future SubReparo Chain will use Polkadot SDK / Substrate as its foundation.

The chain work lives under `chain/`.

Current chain scaffold:

- `chain/README.md`
- `chain/substrate-plan/README.md`
- `chain/pallets/reparodynamics/src/lib.rs`
- `chain/scripts/bootstrap-polkadot-sdk.sh`

The chain is not the scanner. The chain is the repair ledger foundation underneath the scanner.

## Product direction

- v0.1: local project scanner and scar memory
- v0.2: local SQLite repair ledger
- v0.3: website and repo health checks
- v0.4: AI-agent boundary checks
- v0.5: Substrate local chain prototype
- v1.0: downloadable app and server agent

## Principle

SubReparo Immune is for systems the user owns or is authorized to maintain.

It should read carefully, repair cautiously, verify changes, and remember lessons.

Private raw project content should stay local by default. Shared or on-chain records should use safe summaries and hashes.
