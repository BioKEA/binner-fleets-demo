from __future__ import annotations
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ContainerSpec:
    image_tag: str
    cmd: list[str]
    mounts: dict[Path, Path] = field(default_factory=dict)  # host -> container
    env: dict[str, str] = field(default_factory=dict)
    cpus: float = 4.0
    memory_gb: int = 8
    timeout_seconds: int = 1800
    workdir: str = "/work"


@dataclass
class RunResult:
    exit_code: int
    stdout: str
    stderr: str
    runtime_seconds: float


def run_in_container(spec: ContainerSpec) -> RunResult:
    args = [
        "docker", "run", "--rm",
        "--cpus", str(spec.cpus),
        "--memory", f"{spec.memory_gb}g",
        "-w", spec.workdir,
    ]
    for host, container in spec.mounts.items():
        args += ["-v", f"{host}:{container}"]
    for k, v in spec.env.items():
        args += ["-e", f"{k}={v}"]
    args.append(spec.image_tag)
    args.extend(spec.cmd)

    start = time.monotonic()
    proc = subprocess.run(
        args, capture_output=True, text=True, timeout=spec.timeout_seconds
    )
    elapsed = time.monotonic() - start
    return RunResult(
        exit_code=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        runtime_seconds=elapsed,
    )
