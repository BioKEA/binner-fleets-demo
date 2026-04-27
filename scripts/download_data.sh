#!/usr/bin/env bash
# scripts/download_data.sh — fetches STRONG100 + 5G_metaSPAdes into data/
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p data

# --- STRONG100 from Zenodo ---
if [[ ! -d data/strong100 ]]; then
    echo "Downloading STRONG100 (~101 MB)..."
    mkdir -p data/strong100
    cd data/strong100
    curl -L -o strong100.zip "https://zenodo.org/record/6122610/files/strong100.zip"
    unzip -q strong100.zip
    rm strong100.zip
    cd ../..
fi

# --- 5G_metaSPAdes from MetaCoAG repo ---
if [[ ! -d data/5G_metaSPAdes ]]; then
    echo "Downloading 5G_metaSPAdes from MetaCoAG..."
    git clone --depth 1 https://github.com/metagentools/MetaCoAG.git /tmp/metacoag-tmp
    cp -r /tmp/metacoag-tmp/test_data/5G_metaSPAdes data/5G_metaSPAdes 2>/dev/null \
        || cp -r /tmp/metacoag-tmp/tests/data/5G_metaSPAdes data/5G_metaSPAdes
    rm -rf /tmp/metacoag-tmp
fi

echo
echo "Verifying:"
ls -la data/strong100/ | head -20
echo
ls -la data/5G_metaSPAdes/ | head -20
echo "Done."
