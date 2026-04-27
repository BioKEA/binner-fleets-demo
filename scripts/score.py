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


def score_binset(bs: BinSet, contig_markers: dict[str, set[str]]) -> tuple[int, int, list[int]]:
    """Return (total_unique_markers, n_bins, per_bin_marker_counts)."""
    bin_to_contigs: dict[str, list[str]] = defaultdict(list)
    for a in bs.assignments:
        bin_to_contigs[a.bin_id].append(a.contig_id)
    per_bin = []
    for bin_id, contigs in bin_to_contigs.items():
        markers: set[str] = set()
        for c in contigs:
            markers |= contig_markers.get(c, set())
        per_bin.append(len(markers))
    return sum(per_bin), len(per_bin), per_bin


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
    ax.set_xlabel("Total unique single-copy marker Pfams across bins (proxy for total MAG quality)")
    ax.set_title("Binner Leaderboard — STRONG100 (marker-gene proxy)")
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
        total, n_bins, per_bin = score_binset(bs, contig_markers)
        scores[tool] = total
        details[tool] = {
            "wave": pq_path.parent.parent.name,
            "n_bins": n_bins,
            "total_markers": total,
            "mean_markers_per_bin": (total / n_bins) if n_bins else 0,
            "per_bin": per_bin,
        }

    (SCORE_DIR / "leaderboard.json").write_text(json.dumps({"scores": scores, "details": details}, indent=2))
    render_leaderboard(scores, SCORE_DIR / "leaderboard.png")

    print(f"\nLeaderboard:")
    for t, v in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        marker = " *" if t in ("biokea-v0", "biokea") else ""
        print(f"  {v:>6}  {t}{marker}")
    print(f"\nWritten: {SCORE_DIR / 'leaderboard.png'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
