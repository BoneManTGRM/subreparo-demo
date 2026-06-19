# Substrate Integration Notes

## Foundation

SubReparo Chain will be based on Polkadot SDK / Substrate.

The first working chain should be a local solochain or template-based development chain.

## What goes on-chain

On-chain records should be small, bounded, and safe:

- event id;
- reporter account;
- fracture type label;
- severity label;
- evidence hash;
- status;
- block number.

## What stays off-chain

The following should stay local or in private storage by default:

- raw project files;
- raw logs;
- private customer data;
- environment files;
- internal notes;
- anything that could expose a user or business.

## First pallet

The first pallet is `pallet-reparodynamics`.

It currently defines the first repair lifecycle storage model and calls:

- `submit_stress_event`
- `update_repair_status`

## Runtime wiring checklist

When a full Polkadot SDK template exists in `chain/`, wire the pallet into the runtime:

1. Add the pallet to the workspace.
2. Add the pallet to runtime dependencies.
3. Configure `MaxLabelLen` and `MaxHashLen`.
4. Add the pallet to `construct_runtime!`.
5. Run runtime build.
6. Run local node.
7. Submit first repair event.
8. Query storage for the event.

## CLI bridge checklist

After the local chain runs:

1. Add chain RPC configuration to the Python CLI.
2. Add a command to export verified ledger events.
3. Add a command to submit a verified event summary.
4. Store the returned chain event id in the local ledger.
5. Keep private details local.
