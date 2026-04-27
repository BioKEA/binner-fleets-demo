#!/usr/bin/env python3
"""Score every BinSet under output/wave{1,2,3}/ via marker-gene quality."""
from __future__ import annotations
import ast
import json
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from biokea.schema import BinSet

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output"
MARKER_TSV = ROOT / "data" / "strong100" / "marker_gene_stats.tsv"
SCORE_DIR = OUTPUT / "score"


def load_contig_markers(path: Path) -> dict[str, set[str]]:
    """Parse marker_gene_stats.tsv -> {contig_id: set of Pfam IDs}."""
    contig_markers: dict[str, set[str]] = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            contig_id, dict_str = line.split("\t", 1)
        except ValueError:
            continue
        try:
            d = ast.literal_eval(dict_str)
        except (ValueError, SyntaxError):
            d = {}
        markers: set[str] = set()
        for gene_id, pfam_dict in (d or {}).items():
            for pfam_id in (pfam_dict or {}).keys():
                markers.add(pfam_id)
        contig_markers[contig_id] = markers
    return contig_markers


NC_THRESHOLD = 80   # Near-complete: ≥80 unique Pfam markers (≈ ≥80% complete prokaryote)
MQ_THRESHOLD = 40   # Medium-quality: 40–79


def score_binset(bs: BinSet, contig_markers: dict[str, set[str]]) -> dict:
    """Compute per-bin marker counts and aggregate MIMAG-style score.

    Aggregate score = 2 * n_NC_bins + n_MQ_bins.
    This rewards complete genomes (NC bins, ≥80 markers), gives partial credit for
    medium-quality (40–79), and ignores low-quality fragments (<40). It punishes
    over-fragmentation: splitting one good genome into 20 singletons drops most of
    them below the MQ threshold and yields zero score.
    """
    bin_to_contigs: dict[str, list[str]] = defaultdict(list)
    for a in bs.assignments:
        bin_to_contigs[a.bin_id].append(a.contig_id)
    per_bin = []
    n_nc = 0
    n_mq = 0
    for bin_id, contigs in bin_to_contigs.items():
        markers: set[str] = set()
        for c in contigs:
            markers |= contig_markers.get(c, set())
        n = len(markers)
        per_bin.append(n)
        if n >= NC_THRESHOLD:
            n_nc += 1
        elif n >= MQ_THRESHOLD:
            n_mq += 1
    score = 2 * n_nc + n_mq
    return {
        "score": score,
        "n_bins": len(per_bin),
        "n_nc": n_nc,
        "n_mq": n_mq,
        "per_bin": per_bin,
    }


def render_leaderboard(scores: dict[str, int], out_png: Path) -> None:
    items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    tools = [t for t, _ in items]
    vals = [v for _, v in items]
    colors = [
        "#d62728" if t in ("biokea-v0", "biokea") else "#1f77b4"
        for t in tools
    ]
    fig, ax = plt.subplots(figsize=(11, max(4, 0.35 * len(tools) + 1)))
    ax.barh(range(len(tools)), vals, color=colors)
    ax.set_yticks(range(len(tools)))
    ax.set_yticklabels(tools)
    ax.set_xlabel("Score = 2 × NC bins + MQ bins  (NC: ≥80 unique Pfam markers; MQ: 40–79)")
    ax.set_title("Binner Leaderboard — STRONG100 (MIMAG-proxy via marker genes)")
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)


def main() -> int:
    if not MARKER_TSV.exists():
        print(f"ERROR: {MARKER_TSV} not found. Run scripts/download_data.sh first.", file=sys.stderr)
        return 2

    parquet_files = sorted(OUTPUT.glob("wave*/*/bins.parquet"))
    if not parquet_files:
        print("No bin outputs found under output/wave*/. Did you run the demo?", file=sys.stderr)
        return 1

    contig_markers = load_contig_markers(MARKER_TSV)
    print(f"Loaded markers for {len(contig_markers)} contigs")

    SCORE_DIR.mkdir(parents=True, exist_ok=True)
    scores: dict[str, int] = {}
    details: dict[str, dict] = {}
    for pq_path in parquet_files:
        tool = pq_path.parent.name
        bs = BinSet.from_parquet(pq_path)
        result = score_binset(bs, contig_markers)
        scores[tool] = result["score"]
        details[tool] = {"wave": pq_path.parent.parent.name, **result}

    (SCORE_DIR / "leaderboard.json").write_text(json.dumps({"scores": scores, "details": details}, indent=2))
    render_leaderboard(scores, SCORE_DIR / "leaderboard.png")

    print(f"\nLeaderboard (score = 2*NC + MQ):")
    for t, v in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        marker = " *" if t in ("biokea-v0", "biokea") else ""
        d = details[t]
        print(f"  {v:>4}  {t:<20s}  ({d['n_nc']} NC + {d['n_mq']} MQ of {d['n_bins']} bins){marker}")
    print(f"\nWritten: {SCORE_DIR / 'leaderboard.png'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
