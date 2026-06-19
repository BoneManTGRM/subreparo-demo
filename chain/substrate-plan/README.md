# SubReparo Substrate Scaffold Plan

This folder defines how the Polkadot SDK / Substrate foundation should be created when the full chain template is available.

## Current constraint

The connected GitHub tool can edit this repository, but it cannot directly fork the upstream Polkadot SDK repository or create a new GitHub repository.

Because of that, this repo contains:

- the immune scanner in `immune/`;
- the local repair ledger;
- the Substrate design plan;
- the future pallet skeleton and integration notes.

## Target chain layout

When the Polkadot SDK template is copied in, the target layout should become:

```text
chain/
  node/
  runtime/
  pallets/
    reparodynamics/
    scar-memory/
    repair-verification/
  scripts/
  README.md
```

## First runtime objective

The first working chain should support a simple repair lifecycle:

```text
submit_stress_event
classify_fracture
propose_repair
verify_repair
store_scar_memory
```

## Relationship to immune CLI

The Python immune CLI should detect project issues and write a local ledger first.

Later, verified local repair records can be submitted to the Substrate chain as summarized records with evidence hashes.

Private raw project content should stay local unless the user explicitly chooses to publish a safe summary.
