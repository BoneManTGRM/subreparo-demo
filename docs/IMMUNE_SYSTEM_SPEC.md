# SubReparo Immune System Spec

## Product definition

SubReparo Immune is a repair-memory layer for project health.

It watches approved project areas, detects stress signals, creates repair records, verifies fixes, and stores scar memory.

## First protected assets

The first version focuses on assets Cody can build and sell around quickly:

- project folders;
- GitHub repositories;
- websites and landing pages;
- lead forms;
- AI-agent project files;
- deployment configuration.

## First immune functions

### 1. Project scan

Reads approved project files and looks for risky project patterns.

### 2. Scar memory

Turns findings into durable rules.

Example structure:

```text
stress
fracture
repair
verification
scar rule
```

### 3. Local repair ledger

Stores findings as local repair events with:

- status;
- severity;
- source path;
- recommendation;
- evidence hash;
- verification note.

### 4. Verification lifecycle

Repair records move through:

```text
pending -> repaired -> verified
```

or:

```text
pending -> rejected
```

### 5. Chain-ready evidence

Each repair event receives an evidence hash. Later, verified records can be summarized and submitted to SubReparo Chain.

## Modes

### Monitor mode

Only reports findings.

### Ledger mode

Stores repair events locally.

### Guard mode

Future mode. Prepares low-risk repair steps.

### Chain mode

Future mode. Submits verified summaries to the Substrate repair ledger.

## Non-goals for early versions

The early versions should not:

- delete files automatically;
- modify production systems without approval;
- store private raw project content on-chain;
- launch a public token;
- operate on systems the user does not own or manage.

## Target user experience

The intended product feel is:

```text
Download -> choose project -> scan -> record repairs -> verify -> remember
```

The user should not need to understand blockchain details to get value from the first app.
