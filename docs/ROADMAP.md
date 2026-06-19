# SubReparo Immune Roadmap

## v0.1: Local CLI scanner

Goal: create the first working repair-memory prototype.

Deliverables:

- Python CLI
- local project scan
- findings report
- scar-memory writer
- scanner tests
- project README

## v0.2: Website and repo health checks

Goal: make the tool useful for websites and GitHub projects.

Planned features:

- file baseline
- changed-file comparison
- website status check
- link check
- form checklist
- CI checks

## v0.3: AI-agent boundary checks

Goal: make the tool useful for Nova Cortex-style AI wrappers.

Planned features:

- untrusted content labeling
- tool boundary checklist
- instruction-boundary phrase detection
- approval policy file
- agent run repair log

## v0.4: Repair ledger

Goal: move from a local JSONL scar log to a structured local ledger.

Planned features:

- SQLite repair ledger
- scar query command
- repair status lifecycle
- verified repair records
- evidence hash field

## v0.5: Desktop prototype

Goal: make the product easier to use.

Planned features:

- simple desktop dashboard
- protected project list
- findings timeline
- scar memory viewer
- approval queue

## v1.0: Downloadable repair-memory layer

Goal: package SubReparo Immune so a user can download it, connect a project, and let it watch approved project areas.

Planned features:

- installer
- background watcher
- dashboard
- repair suggestions
- update system
- optional scar-memory sync
