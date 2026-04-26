from pathlib import Path

from biokea.binners._base import BinnerAdapter, AdapterResult


def test_adapter_protocol_attributes():
    """Any BinnerAdapter must expose these class attributes."""
    assert hasattr(BinnerAdapter, "tool_name")
    assert hasattr(BinnerAdapter, "tool_version")
    assert hasattr(BinnerAdapter, "image_tag")


def test_adapter_result_dataclass():
    r = AdapterResult(
        success=True,
        binset_path=Path("output/wave1/metabat2/bins.parquet"),
        runtime_seconds=42.0,
        peak_memory_mb=1024,
        error=None,
    )
    assert r.success
    assert r.error is None


def test_adapter_result_failure():
    r = AdapterResult(
        success=False,
        binset_path=None,
        runtime_seconds=0.0,
        peak_memory_mb=0,
        error="Smoke test failed: missing libgd",
    )
    assert not r.success
    assert "libgd" in r.error
