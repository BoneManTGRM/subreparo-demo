# SubReparo Chain

This folder is reserved for the Polkadot SDK / Substrate foundation of SubReparo.

## Decision

SubReparo will use **Polkadot SDK / Substrate** as its blockchain foundation.

The first chain target is a local/private solochain prototype, not a public token launch.

## Why Polkadot SDK / Substrate

Polkadot SDK / Substrate is the right foundation because it provides:

- a modular runtime architecture;
- FRAME pallets for custom chain logic;
- local development chains;
- a path from solochain prototype to parachain-ready design;
- Rust-based runtime modules;
- benchmarking and weight systems;
- governance and upgrade paths;
- future interoperability options.

## First chain purpose

The SubReparo chain is not the first immune scanner. The scanner lives in `immune/`.

The chain becomes the **repair ledger** underneath SubReparo Immune.

It should eventually record:

- stress events;
- fracture classifications;
- repair proposals;
- verification results;
- scar memory hashes;
- repair efficiency scores;
- reporter/verifier reputation.

## Build order

### Phase 1: Immune CLI

The current `immune/` package detects project stress signals and writes local scar memory.

### Phase 2: Local repair ledger

Before a full blockchain, add a structured local ledger for repair events.

### Phase 3: SubReparo solochain

Initialize a Polkadot SDK solochain template and rename it into:

```text
subreparo-node
subreparo-runtime
pallet-reparodynamics
pallet-scar-memory
pallet-repair-verification
```

### Phase 4: Chain integration

Allow SubReparo Immune to submit verified repair summaries and evidence hashes to the local chain.

### Phase 5: Parachain-ready branch

After the solochain works, create a parachain-ready version.

## Safety rule

No public token, public mainnet, bridge, or real-value asset should be launched until the runtime is tested, benchmarked, reviewed, and audited.
