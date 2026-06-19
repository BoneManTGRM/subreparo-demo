# SubReparo Chain Milestones

## Milestone 0: Foundation decision

Status: selected.

Foundation: Polkadot SDK / Substrate.

## Milestone 1: Local repair ledger

Goal: bridge the current Python immune scanner to a structured repair-event format.

Deliverables:

- repair event schema;
- local SQLite or JSON repair ledger;
- evidence hash field;
- verified / pending / rejected repair status;
- CLI command for repair records.

## Milestone 2: Polkadot SDK solochain scaffold

Goal: create the first Substrate chain scaffold.

Deliverables:

- `subreparo-node`;
- `subreparo-runtime`;
- custom token symbol for dev chain;
- local node run instructions;
- first runtime build.

## Milestone 3: pallet-reparodynamics

Goal: implement the repair lifecycle on-chain.

Core extrinsics:

```text
submit_stress_event
classify_fracture
propose_repair
verify_repair
store_scar_memory
```

Core events:

```text
StressEventSubmitted
FractureClassified
RepairProposed
RepairVerified
ScarMemoryStored
```

## Milestone 4: SubReparo Immune integration

Goal: let the CLI submit verified summaries to the local chain.

Deliverables:

- chain RPC config;
- CLI submit command;
- evidence hash generation;
- local dev account support;
- query command for repair records.

## Milestone 5: Private testnet

Goal: run more than one node.

Deliverables:

- private chain spec;
- 2-4 local or VPS nodes;
- basic monitoring;
- repair-event dashboard.

## Milestone 6: Parachain-ready exploration

Goal: assess whether the runtime should be ported to a parachain template.

Deliverables:

- parachain feasibility notes;
- runtime portability checklist;
- cost and security review.

## Milestone 7: Security review before public release

Goal: do not expose real users or assets before review.

Deliverables:

- tests;
- benchmarks;
- storage bounds;
- origin checks;
- rate limits;
- review checklist;
- documented emergency process.
