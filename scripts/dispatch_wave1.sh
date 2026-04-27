#!/usr/bin/env bash
# scripts/dispatch_wave1.sh — fans out 16 Wave 1 sessions via Claude Fleets
#
# Usage: bash scripts/dispatch_wave1.sh [batch_size]
#
# Each session runs the /integrate-binner skill on one tool.
# Sessions write to wave1/<tool> sub-branches; finalize_wave1.sh merges them.

set -euo pipefail

BATCH_SIZE="${1:-16}"  # default: all in parallel

WAVE1_TOOLS=(
    metabat2 concoct maxbin2
    vamb semibin2 comebin genomeface taxvamb metabinner metadecoder
    graphbin2 metacoag graphmb unitigbin
    mycc cocacola
)

if [[ "${#WAVE1_TOOLS[@]}" -ne 16 ]]; then
    echo "ERROR: Wave 1 tool list must have 16 entries; has ${#WAVE1_TOOLS[@]}." >&2
    exit 1
fi

dispatch() {
    local tool="$1"
    echo "Dispatching: $tool"
    claude --bg "/integrate-binner $tool"
}

if [[ "$BATCH_SIZE" -ge 16 ]]; then
    for tool in "${WAVE1_TOOLS[@]}"; do
        dispatch "$tool"
    done
else
    n=0
    for tool in "${WAVE1_TOOLS[@]}"; do
        dispatch "$tool"
        n=$((n+1))
        if (( n % BATCH_SIZE == 0 )) && (( n < ${#WAVE1_TOOLS[@]} )); then
            echo "  (waiting 60s before next batch...)"
            sleep 60
        fi
    done
fi

echo
echo "Wave 1 dispatched: ${#WAVE1_TOOLS[@]} sessions."
echo "Run 'claude agents' to monitor."
