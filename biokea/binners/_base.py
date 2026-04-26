from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Protocol


@dataclass
class AdapterResult:
    success: bool
    binset_path: Optional[Path]
    runtime_seconds: float
    peak_memory_mb: int
    error: Optional[str] = None


class BinnerAdapter(Protocol):
    """Per-binner adapter contract.

    Each `biokea/binners/<tool>.py` defines a class implementing this protocol.
    The class is a singleton namespace — its methods are class-level operations
    keyed off its class attributes.
    """

    tool_name: str = ""
    tool_version: str = ""
    image_tag: str = ""

    @classmethod
    def smoke_test(cls, data_dir: Path, output_dir: Path) -> AdapterResult:
        """Run on the 5G_metaSPAdes canary dataset. Must finish < 60s."""
        ...

    @classmethod
    def run(cls, data_dir: Path, output_dir: Path) -> AdapterResult:
        """Run on STRONG100. Writes a BinSet to output_dir/bins.parquet."""
        ...
