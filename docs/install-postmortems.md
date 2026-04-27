# Install Postmortems — pre-flight findings

This document records every binner that failed to install cleanly during pre-flight, with the exact root cause and the unblock fix to apply during the live demo (or in a follow-up).

The two **planned-block** entries are the ones to reach for during the recording when their Fleet session goes amber. Operator can `space`-peek, paste the fix, and watch the rebuild succeed.

---

## Summary

| Tool | Pre-flight status | Failure type | Resolution |
|---|---|---|---|
| metabat2 | ✅ built | conda channel + bad version pin | fixed in pre-flight |
| concoct | ✅ built | conda channel | fixed in pre-flight |
| maxbin2 | ✅ built | conda channel | fixed in pre-flight |
| **vamb** | ❌ planned-block | pycoverm dep needs Rust + maturin (build-isolation) | **live unblock — see below** |
| semibin2 | ✅ built | none | clean |
| comebin | ✅ built | bedtools version pin in bioconda recipe | fixed in pre-flight (git clone + loose deps) |
| genomeface | ✅ built | none | clean (placeholder) |
| **taxvamb** | ❌ planned-block | same as vamb (shares pycoverm dep) | **live unblock — see below** |
| metabinner | ✅ built | none | clean |
| metadecoder | ✅ built | not on PyPI | fixed in pre-flight (git+ install) |
| graphbin2 | ✅ built | none | clean |
| metacoag | ✅ built | none | clean |
| graphmb | ✅ built | tensorflow vs torch resolver conflict | fixed in pre-flight (`--no-deps`) |
| unitigbin | ✅ built | none | clean (image is thin shell — runtime-validate during demo) |
| mycc | ✅ built | none | clean (image is thin shell — runtime-validate during demo) |
| cocacola | ✅ built | none | clean (image is thin shell — runtime-validate during demo) |
| das_tool | ✅ built | conda channel | fixed in pre-flight |
| metawrap | ✅ built | conda channel | fixed in pre-flight |
| magscot | ✅ built | not on bioconda | fixed in pre-flight (git clone + r-base) |
| binette | ✅ built | none | clean |

Wave 1: 14 of 16 cleanly cached, 2 planned-block (vamb, taxvamb).
Wave 2: 4 of 4 cleanly cached.

---

## Planned-block #1 — vamb

**Symptom on camera:** Wave 1 session for `vamb` goes amber within ~30 seconds. `space` to peek shows a build error mentioning `pycoverm` and `metadata-generation-failed`.

**Root cause:** vamb's PyPI package depends on `pycoverm>=0.6.2`, which is a Rust-based extension. The build isolation layer in pip can't generate metadata without a Rust toolchain *and* maturin (the Rust-Python glue) being available *during* the metadata phase. Apt's rustc/cargo aren't enough — pip's PEP 517 build needs maturin in the build environment.

**Unblock fix to paste in peek reply:**

```
Replace docker/vamb/Dockerfile with:

FROM biokea-binner-base:1.0
USER root
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable \
    && . "$HOME/.cargo/env"
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install --no-cache-dir maturin
RUN pip install --no-cache-dir vamb
WORKDIR /work
```

Then rebuild: `docker build -t biokea-binner-base:1.0-vamb docker/vamb/`.

**Estimated unblock-to-green time on camera:** ~5 min (rustup install + cargo compile of pycoverm).

---

## Planned-block #2 — taxvamb

**Symptom on camera:** same as vamb, with `vamb>=5` mentioned in the install line.

**Root cause:** identical to vamb (taxvamb is a subcommand of `vamb>=5`, shares the pycoverm dependency).

**Unblock fix to paste in peek reply:**

```
Replace docker/taxvamb/Dockerfile with:

FROM biokea-binner-base:1.0
USER root
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable \
    && . "$HOME/.cargo/env"
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install --no-cache-dir maturin
RUN pip install --no-cache-dir "vamb>=5"
WORKDIR /work
```

Then rebuild: `docker build -t biokea-binner-base:1.0-taxvamb docker/taxvamb/`.

---

## Notes for operator during recording

- These are the *only* two tools where the pre-built Docker image is missing. All other 18 are already cached locally — their Wave 1 sessions just need to `docker run` and parse output.
- Both planned-blocks share the same root cause (pycoverm + Rust + maturin), so a viewer who watches the vamb unblock should *recognize* the same pattern when taxvamb blocks. Possible narration: "same fix for taxvamb — vamb is its parent package."
- After both unblocks, all 20 tools have working images. Wave 2 (refiners) and Wave 3 (biokea v0) have no install dependencies of their own.
