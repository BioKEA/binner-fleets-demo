#!/usr/bin/env bash
# scripts/run_demo.sh — full reproducer: pre-flight, all waves, score.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "=== STEP 1: Download data ==="
bash scripts/download_data.sh

echo "=== STEP 2: Build Docker images ==="
bash scripts/prebuild_images.sh

echo "=== STEP 3: Wave 1 (parallel, 16 sessions) ==="
bash scripts/dispatch_wave1.sh

echo "Waiting for Wave 1 to complete..."
echo "(Monitor in another terminal: 'claude agents')"
echo "Press Enter when all Wave 1 sessions are 'done' or 'failed'."
read -r

echo "=== STEP 4: Finalize Wave 1 (merge sub-branches) ==="
bash scripts/finalize_wave1.sh

echo "=== STEP 5: Wave 2 (4 refiners) ==="
bash scripts/dispatch_wave2.sh

echo "Waiting for Wave 2 to complete... press Enter when done."
read -r

echo "=== STEP 6: Wave 3 (biokea v0) ==="
bash scripts/dispatch_wave3.sh

echo "=== STEP 7: Score ==="
.venv/bin/python scripts/score.py

echo "=== DONE. See output/score/leaderboard.png ==="
