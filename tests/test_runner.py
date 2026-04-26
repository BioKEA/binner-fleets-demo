from pathlib import Path
from biokea.runner import run_in_container, ContainerSpec


def test_container_spec_construction():
    spec = ContainerSpec(
        image_tag="alpine:3.19",
        cmd=["echo", "hello"],
        mounts={Path("/tmp"): Path("/data")},
        timeout_seconds=10,
    )
    assert spec.image_tag == "alpine:3.19"
    assert spec.cmd == ["echo", "hello"]


def test_run_simple_container_succeeds(tmp_path):
    spec = ContainerSpec(
        image_tag="alpine:3.19",
        cmd=["echo", "hello"],
        mounts={tmp_path: Path("/data")},
        timeout_seconds=10,
    )
    res = run_in_container(spec)
    assert res.exit_code == 0
    assert "hello" in res.stdout
    assert res.runtime_seconds > 0


def test_run_failing_container_returns_nonzero(tmp_path):
    spec = ContainerSpec(
        image_tag="alpine:3.19",
        cmd=["sh", "-c", "exit 17"],
        mounts={tmp_path: Path("/data")},
        timeout_seconds=10,
    )
    res = run_in_container(spec)
    assert res.exit_code == 17
