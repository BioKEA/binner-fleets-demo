---
name: integrate-binner
description: Integrate a single metagenome binner into the BioKEA binner-fleets-demo repo. Reads the per-tool spec.yaml, builds the Dockerfile, smoke-tests on 5G_metaSPAdes, runs on STRONG100, parses output to the unified BinSet schema, writes a 50-LOC adapter file, commits to wave1/<tool> sub-branch.
---

# Integrate Binner

You are integrating a single metagenome binner into BioKEA's binner-fleets-demo repo. The tool name is provided as your argument.

## Inputs

- **Tool name:** the argument passed to this skill (e.g., `metabat2`, `concoct`, `mycc`).
- **Per-tool stub:** `tools/<tool>/spec.yaml` — repo URL, install hint, CLI invocation, output format hint. Read this first.
- **Dockerfile draft:** `docker/<tool>/Dockerfile` — first-pass Dockerfile already authored. May need amendment.
- **Smoke test data:** `data/5G_metaSPAdes/` (5 genomes, ~30s run).
- **Demo data:** `data/strong100/` (~100 species; the real run).
- **Schema:** `biokea/schema.py` defines `ContigAssignment` and `BinSet`. Output must conform.
- **Base adapter protocol:** `biokea/binners/_base.py` defines `BinnerAdapter`. Your adapter must implement it.

## Procedure

1. **Read the spec stub.** Open `tools/<tool>/spec.yaml`. Confirm repo URL, install method, CLI pattern, expected output format.

2. **Build the Docker image.**
   - `docker build -t biokea-binner-base:1.0-<tool> -f docker/<tool>/Dockerfile docker/<tool>/`
   - If the build fails: read the error, amend the Dockerfile, rebuild. Common failure modes: missing system packages, pinned dependency conflicts, Python 2-only tools requiring a python2-legacy base.
   - **STOP and surface the failure if the same error recurs after one amendment.** This is when the operator should peek (`space`) and unblock you.

3. **Smoke test on 5G_metaSPAdes.**
   - Mount `data/5G_metaSPAdes/` into the container, run the tool on it.
   - Must complete in < 60 seconds (otherwise the install is broken).
   - On failure: STOP, surface the error, await peek-and-unblock.

4. **Run on STRONG100.**
   - Mount `data/strong100/` into the container, run the tool.
   - Capture: stdout, stderr, runtime, peak memory.

5. **Parse the tool's output to a `BinSet`.**
   - Tool output formats vary: per-bin FASTA files, contig-to-bin TSV, clusters.tsv, etc.
   - Map each contig to its assigned bin id. Construct `ContigAssignment(contig_id, bin_id)` per row.
   - Wrap in `BinSet(tool=<name>, tool_version=<v>, sample="strong100", runtime_seconds=<t>, peak_memory_mb=<m>, assignments=[...])`.

6. **Write the unified output.**
   - `bs.to_parquet("output/wave1/<tool>/bins.parquet")`

7. **Write the adapter file `biokea/binners/<tool>.py`.**
   - ~50 LOC implementing the `BinnerAdapter` protocol from `biokea/binners/_base.py`.
   - Class methods: `smoke_test(data_dir, output_dir)`, `run(data_dir, output_dir)`. Both return `AdapterResult`.
   - Use `biokea.runner.run_in_container` to invoke the Docker image.
   - The adapter encapsulates: image_tag, CLI invocation, output-parsing logic.

8. **Commit to a per-tool sub-branch.**
   - Create branch: `git checkout -b wave1/<tool>`
   - Stage: `biokea/binners/<tool>.py`, `output/wave1/<tool>/bins.parquet` (output committed only if size < 5 MB; otherwise gitignored).
   - Commit: `git commit -m "feat(binners): add <tool> adapter and bin output"`
   - Push: `git push origin wave1/<tool>`
   - **Do NOT commit to `wave1` directly.** The finalize step does fast-forward merges in deterministic order.

9. **Report done.** Surface a one-line summary: tool name, runtime, n_bins produced, success/failure.

## On any failure: STOP

Do not retry-loop indefinitely. After one or two amendment attempts, surface the error clearly and wait. The operator's `space`-to-peek workflow is the unblock mechanism.
