"""biokea v0 ensembler — DAS_Tool-style SCG-scored bin selection.

For v0: bin score = number of contigs in the bin (a stand-in for SCG-based
quality score). Iteratively select the highest-scoring bin from any input
binset, mask its contigs, repeat.

A CheckM2 quality filter is a deferred refinement; v0 uses min-bin-size as a
placeholder.
"""
from __future__ import annotations
from collections import defaultdict
from typing import Iterable

from biokea.schema import BinSet, ContigAssignment

MIN_BIN_SIZE = 2  # placeholder for CheckM2 quality filter


def _score_bins(binsets: Iterable[BinSet]) -> list[tuple[int, str, str, set[str]]]:
    """Return list of (score, tool, bin_id, contigs) tuples, sorted descending."""
    scored = []
    for bs in binsets:
        bin_to_contigs: dict[str, set[str]] = defaultdict(set)
        for a in bs.assignments:
            bin_to_contigs[a.bin_id].add(a.contig_id)
        for bin_id, contigs in bin_to_contigs.items():
            scored.append((len(contigs), bs.tool, bin_id, contigs))
    scored.sort(key=lambda t: t[0], reverse=True)
    return scored


def ensemble_v0(binsets: list[BinSet]) -> BinSet:
    """Select the best non-overlapping bins greedily, score-descending."""
    if not binsets:
        return BinSet(
            tool="biokea-v0",
            tool_version="0.1.0",
            sample="strong100",
            runtime_seconds=0.0,
            peak_memory_mb=0,
            assignments=[],
        )

    scored = _score_bins(binsets)
    used: set[str] = set()
    out_assignments: list[ContigAssignment] = []
    next_bin_idx = 0

    for score, tool, bin_id, contigs in scored:
        if score < MIN_BIN_SIZE:
            continue
        unused = contigs - used
        if len(unused) < MIN_BIN_SIZE:
            continue
        out_bin_id = f"biokea_bin_{next_bin_idx}"
        next_bin_idx += 1
        for contig in sorted(unused):
            out_assignments.append(
                ContigAssignment(contig_id=contig, bin_id=out_bin_id)
            )
        used |= unused

    sample = binsets[0].sample
    return BinSet(
        tool="biokea-v0",
        tool_version="0.1.0",
        sample=sample,
        runtime_seconds=sum(bs.runtime_seconds for bs in binsets),
        peak_memory_mb=max(bs.peak_memory_mb for bs in binsets),
        assignments=out_assignments,
    )
