# SubReparo Immune Architecture

SubReparo Immune is designed as a layered repair-memory system.

## Core loop

```text
Observe -> Detect -> Classify -> Prepare Repair -> Verify -> Store Scar Memory -> Adapt
```

## Layers

### 1. Sensors

Sensors read approved project locations and collect health signals.

Initial sensors:

- folder scanner
- configuration file checker
- project text scanner
- future website health checker
- future AI-agent boundary checker

### 2. Classifier

The classifier turns raw signals into fracture categories.

Initial categories:

- sensitive local file present
- token-looking string present
- instruction-boundary risk phrase present
- project configuration risk

### 3. Repair planner

The repair planner recommends safe next actions.

The v0 version does not make destructive changes. It prepares guidance and scar-memory rules.

### 4. Verification

Verification confirms that the problem no longer appears after repair.

Initial verification method:

- re-run the scanner
- compare before and after findings

### 5. Scar memory

Scar memory records lessons as JSON Lines in `.subreparo/scar_memory.jsonl`.

Each scar memory record stores:

- stress
- fracture
- repair
- verification
- future rule
- source path
- created timestamp

### 6. Future ledger

Later versions can sync verified scar memory into a local or blockchain-based SubReparo repair ledger.

Private project details should stay local by default. Shared records should use summaries and hashes rather than private raw content.

## Safety model

SubReparo Immune is for systems the user owns or is authorized to maintain.

Default mode is monitor-only.

Risky changes should require approval.
