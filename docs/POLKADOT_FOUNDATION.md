# Polkadot SDK Foundation

## Foundation decision

SubReparo will use **Polkadot SDK / Substrate** as the foundation for its repair-ledger network.

The product has two layers:

1. **SubReparo Immune**: downloadable scanner / repair-memory tool.
2. **SubReparo Chain**: Polkadot SDK / Substrate-based repair ledger.

## Role of the chain

The chain should not scan files directly.

The chain should store verified repair records and scar-memory proofs.

Off-chain tools detect and repair problems. The chain records summaries, hashes, reputation, and verification results.

## Target architecture

```text
SubReparo Immune CLI / app / agent
        |
        v
Local repair ledger
        |
        v
SubReparo Chain API
        |
        v
Polkadot SDK / Substrate runtime
        |
        v
Repair pallets + scar memory + verification events
```

## Initial runtime modules

### pallet-reparodynamics

Stores the basic repair lifecycle:

- stress detected;
- fracture classified;
- repair proposed;
- repair verified;
- scar memory stored.

### pallet-scar-memory

Stores durable lessons and evidence hashes.

Private details should stay off-chain. The chain should store summaries and hashes.

### pallet-repair-verification

Tracks whether a repair was verified, rejected, or still pending.

### pallet-repair-reputation

Tracks reporters and verifiers over time.

This must start conservatively. Reputation should not control consensus in the first version.

## First local chain milestone

The first blockchain milestone is:

```text
Run a local SubReparo solochain.
Submit a repair event.
Verify the repair event.
Store scar memory.
Query the result.
```

## Repo strategy

Preferred final repo split:

```text
subreparo-immune  -> app / scanner / AI shield / server agent
subreparo-node    -> Polkadot SDK / Substrate chain
```

Current repo can temporarily hold both layers while the project is young.

## Non-goals for the first chain version

The first chain version should not include:

- token sale;
- public mainnet;
- bridge;
- DeFi;
- EVM compatibility;
- automatic destructive actions;
- public storage of private logs or secrets.

## Principle

Build the immune layer first. Use the chain as the verified repair memory underneath it.
