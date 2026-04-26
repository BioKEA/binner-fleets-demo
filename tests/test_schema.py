from biokea.schema import ContigAssignment, BinSet


def test_contig_assignment_minimal():
    a = ContigAssignment(contig_id="contig_1", bin_id="bin_3")
    assert a.contig_id == "contig_1"
    assert a.bin_id == "bin_3"
    assert a.confidence is None


def test_contig_assignment_with_confidence():
    a = ContigAssignment(contig_id="c1", bin_id="b1", confidence=0.87)
    assert a.confidence == 0.87


def test_binset_construction():
    bs = BinSet(
        tool="metabat2",
        tool_version="2.15",
        sample="strong100",
        runtime_seconds=42.5,
        peak_memory_mb=1024,
        assignments=[ContigAssignment(contig_id="c1", bin_id="b1")],
    )
    assert bs.tool == "metabat2"
    assert len(bs.assignments) == 1


def test_binset_to_parquet_and_back(tmp_path):
    bs = BinSet(
        tool="metabat2",
        tool_version="2.15",
        sample="strong100",
        runtime_seconds=42.5,
        peak_memory_mb=1024,
        assignments=[
            ContigAssignment(contig_id="c1", bin_id="b1"),
            ContigAssignment(contig_id="c2", bin_id="b1"),
            ContigAssignment(contig_id="c3", bin_id="b2", confidence=0.9),
        ],
    )
    path = tmp_path / "bins.parquet"
    bs.to_parquet(path)
    assert path.exists()

    restored = BinSet.from_parquet(path)
    assert restored.tool == bs.tool
    assert restored.tool_version == bs.tool_version
    assert restored.sample == bs.sample
    assert restored.runtime_seconds == bs.runtime_seconds
    assert restored.peak_memory_mb == bs.peak_memory_mb
    assert len(restored.assignments) == 3
    assert restored.assignments[2].confidence == 0.9
