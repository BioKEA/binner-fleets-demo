#!/usr/bin/env bash
# scripts/dispatch_wave2.sh — 4 refiner sessions, after Wave 1 completes
set -euo pipefail

cd "$(dirname "$0")/.."

WAVE2_REFINERS=(das_tool metawrap magscot binette)

WAVE1_OUTPUTS=$(ls output/wave1/*/bins.parquet 2>/dev/null | wc -l)
if [[ "$WAVE1_OUTPUTS" -lt 1 ]]; then
    echo "ERROR: no wave1 outputs found. Wave 2 needs Wave 1 to be done." >&2
    exit 1
fi
echo "Wave 1 has $WAVE1_OUTPUTS outputs ready."

for refiner in "${WAVE2_REFINERS[@]}"; do
    echo "Dispatching refiner: $refiner"
    claude --bg "/integrate-binner $refiner"
done

echo "Wave 2 dispatched."
