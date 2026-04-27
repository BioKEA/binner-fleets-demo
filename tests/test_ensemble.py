from pathlib import Path
from biokea.schema import BinSet, ContigAssignment
from biokea.ensemble import ensemble_v0


def _binset(tool: str, contig_to_bin: dict[str, str]) -> BinSet:
    return BinSet(
        tool=tool,
        tool_version="test",
        sample="strong100",
        runtime_seconds=1.0,
        peak_memory_mb=1,
        assignments=[
            ContigAssignment(contig_id=c, bin_id=b)
            for c, b in contig_to_bin.items()
        ],
    )


def test_ensemble_picks_larger_bin():
    """Given two binsets, the ensembler prefers the bin covering more contigs."""
    a = _binset("toolA", {"c1": "b1", "c2": "b1", "c3": "b1", "c4": "b1"})
    b = _binset("toolB", {"c1": "x1", "c2": "x2", "c3": "x3", "c4": "x4"})
    result = ensemble_v0([a, b])
    # toolA's b1 is one big bin; toolB has four singletons. The ensembler
    # should select b1 first (higher score), then have nothing left.
    assert result.tool == "biokea-v0"
    assert len({a.bin_id for a in result.assignments}) == 1
    assert len(result.assignments) == 4


def test_ensemble_handles_disjoint_contigs():
    a = _binset("toolA", {"c1": "b1", "c2": "b1"})
    b = _binset("toolB", {"c3": "b1", "c4": "b1"})
    result = ensemble_v0([a, b])
    # Both bins are equally sized — both should appear in the output.
    assert len(result.assignments) == 4
    assert len({a.bin_id for a in result.assignments}) == 2


def test_ensemble_writes_parquet(tmp_path):
    a = _binset("toolA", {"c1": "b1", "c2": "b1"})
    out = tmp_path / "biokea" / "bins.parquet"
    result = ensemble_v0([a])
    result.to_parquet(out)
    assert out.exists()
