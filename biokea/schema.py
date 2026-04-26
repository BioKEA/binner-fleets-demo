from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pyarrow as pa
import pyarrow.parquet as pq


@dataclass
class ContigAssignment:
    contig_id: str
    bin_id: str
    confidence: Optional[float] = None


@dataclass
class BinSet:
    tool: str
    tool_version: str
    sample: str
    runtime_seconds: float
    peak_memory_mb: int
    assignments: list[ContigAssignment] = field(default_factory=list)

    def to_parquet(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        n = len(self.assignments)
        table = pa.table(
            {
                "contig_id": [a.contig_id for a in self.assignments],
                "bin_id": [a.bin_id for a in self.assignments],
                "confidence": [a.confidence for a in self.assignments],
                "tool": [self.tool] * n,
                "tool_version": [self.tool_version] * n,
                "sample": [self.sample] * n,
                "runtime_seconds": [self.runtime_seconds] * n,
                "peak_memory_mb": [self.peak_memory_mb] * n,
            }
        )
        pq.write_table(table, path)

    @classmethod
    def from_parquet(cls, path: str | Path) -> "BinSet":
        path = Path(path)
        table = pq.read_table(path)
        d = table.to_pydict()
        if not d["tool"]:
            raise ValueError(f"Empty BinSet at {path}")
        assignments = [
            ContigAssignment(
                contig_id=d["contig_id"][i],
                bin_id=d["bin_id"][i],
                confidence=d["confidence"][i],
            )
            for i in range(len(d["contig_id"]))
        ]
        return cls(
            tool=d["tool"][0],
            tool_version=d["tool_version"][0],
            sample=d["sample"][0],
            runtime_seconds=d["runtime_seconds"][0],
            peak_memory_mb=d["peak_memory_mb"][0],
            assignments=assignments,
        )
