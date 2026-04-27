#!/usr/bin/env bash
# scripts/dispatch_wave3.sh — single biokea v0 ensembler run
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p output/wave3/biokea-v0

.venv/bin/python -c "
from pathlib import Path
from biokea.schema import BinSet
from biokea.ensemble import ensemble_v0
import time

t0 = time.monotonic()
binsets = [BinSet.from_parquet(p) for p in Path('output/wave1').glob('*/bins.parquet')]
print(f'Loaded {len(binsets)} input binsets')
result = ensemble_v0(binsets)
result.runtime_seconds = time.monotonic() - t0
result.to_parquet('output/wave3/biokea-v0/bins.parquet')
n_unique_bins = len({a.bin_id for a in result.assignments})
print(f'biokea-v0 produced {n_unique_bins} bins from {len(result.assignments)} contig assignments')
"
