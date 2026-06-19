#!/usr/bin/env bash
set -euo pipefail

# This script documents the intended local setup flow for the SubReparo chain.
# It does not run automatically in CI.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WORK_DIR="$ROOT_DIR/.external"
SDK_DIR="$WORK_DIR/polkadot-sdk"

mkdir -p "$WORK_DIR"

if [ ! -d "$SDK_DIR/.git" ]; then
  git clone https://github.com/paritytech/polkadot-sdk.git "$SDK_DIR"
else
  git -C "$SDK_DIR" pull --ff-only
fi

cat <<'MSG'
Polkadot SDK has been downloaded into .external/polkadot-sdk.

Next manual step:
1. Locate the current official solochain or parachain template in the SDK checkout.
2. Copy the template into chain/.
3. Rename the node/runtime for SubReparo.
4. Add chain/pallets/reparodynamics to the runtime.

The GitHub connector cannot fork upstream repos directly, so this script preserves the reproducible local path.
MSG
