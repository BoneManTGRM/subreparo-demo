# pallet-reparodynamics

This is the first FRAME pallet skeleton for the SubReparo repair lifecycle.

## Purpose

The pallet records summarized repair events from SubReparo Immune and future agents.

It starts with:

- `submit_stress_event`
- `update_repair_status`
- bounded labels
- bounded evidence hashes
- pending / repaired / verified / rejected status values

## Important

This pallet is a scaffold until the full Polkadot SDK workspace is copied into `chain/`.

The next step is to place this pallet inside a working Polkadot SDK solochain template and wire it into the runtime.

## Private data rule

Do not put raw private project files, logs, or user secrets on-chain.

Only safe summaries and hashes should be submitted.
