#!/usr/bin/env bash
# scripts/prebuild_images.sh — pre-builds biokea-binner-base + 20 per-tool images
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p /tmp/binner-build-logs
echo > /tmp/binner-build-failures.txt

echo "=== STEP 1: Building base image (biokea-binner-base:1.0) ==="
if docker image inspect biokea-binner-base:1.0 >/dev/null 2>&1; then
    echo "  ⤳ already built, skipping"
else
    docker build -t biokea-binner-base:1.0 docker/base/ 2>&1 | tee /tmp/binner-build-logs/base.log
fi

echo "=== STEP 2: Building python2-legacy variant ==="
if docker image inspect biokea-binner-base:1.0-python2-legacy >/dev/null 2>&1; then
    echo "  ⤳ already built, skipping"
else
    docker build -t biokea-binner-base:1.0-python2-legacy docker/python2-legacy/ 2>&1 | tee /tmp/binner-build-logs/python2-legacy.log
fi

echo "=== STEP 3: Building 20 per-tool images ==="
TOOLS=(metabat2 concoct maxbin2 vamb semibin2 comebin genomeface taxvamb \
       metabinner metadecoder graphbin2 metacoag graphmb unitigbin \
       mycc cocacola das_tool metawrap magscot binette)

for tool in "${TOOLS[@]}"; do
    if docker image inspect "biokea-binner-base:1.0-$tool" >/dev/null 2>&1; then
        echo "  ⤳ $tool (already built, skipping)"
        continue
    fi
    echo
    echo "--- Building $tool ---"
    if docker build -t "biokea-binner-base:1.0-$tool" "docker/$tool/" 2>&1 | tee "/tmp/binner-build-logs/$tool.log"; then
        echo "  ✓ $tool"
    else
        echo "  ✗ $tool (BUILD FAILED — see /tmp/binner-build-logs/$tool.log)"
        echo "$tool" >> /tmp/binner-build-failures.txt
    fi
done

echo
echo "=== Summary ==="
echo "Successful: $(docker images --format '{{.Repository}}:{{.Tag}}' | grep -c '^biokea-binner-base:1.0-')"
echo "Failures recorded: $(wc -l < /tmp/binner-build-failures.txt)"
if [[ -s /tmp/binner-build-failures.txt ]]; then
    echo "Failed tools (will need live unblock during demo):"
    cat /tmp/binner-build-failures.txt
fi
