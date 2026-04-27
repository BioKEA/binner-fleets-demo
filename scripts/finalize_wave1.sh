#!/usr/bin/env bash
# scripts/finalize_wave1.sh — fast-forward merge wave1/<tool> branches into wave1
set -euo pipefail

cd "$(dirname "$0")/.."

# Deterministic order matches dispatch_wave1.sh
ORDER=(metabat2 concoct maxbin2 vamb semibin2 comebin genomeface taxvamb \
       metabinner metadecoder graphbin2 metacoag graphmb unitigbin mycc cocacola)

git fetch --all --prune
if ! git rev-parse --verify wave1 >/dev/null 2>&1; then
    git checkout -b wave1 main
    git push -u origin wave1
else
    git checkout wave1
fi

for tool in "${ORDER[@]}"; do
    branch="wave1/$tool"
    if git rev-parse --verify "origin/$branch" >/dev/null 2>&1; then
        echo "Merging $branch -> wave1"
        git merge --ff-only "origin/$branch" || {
            echo "  (non-FF; using merge commit for $branch)"
            git merge --no-ff "origin/$branch" -m "merge: $branch into wave1"
        }
    else
        echo "  (skipping $branch — not present)"
    fi
done

git push origin wave1
echo "Done. wave1 has $(git log --oneline main..wave1 | wc -l) commits ahead of main."
