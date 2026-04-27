# Recording Day Runbook — Binner Fleets Demo (v2: chat-centric)

This is the operator's hands-on script. **Single window, chat-centric.** The Fleets-style fan-out happens inside a Claude Code chat session via Claude's Task tool; sub-agents appear in the `/agents` "Running" tab, which is the hero shot.

---

## 0. Pre-record checklist (do once, off-camera)

```bash
cd /Users/seanjungbluth/Desktop/binner-fleets-demo

git status                  # → clean
git pull --ff-only          # → up to date
git branch -D wave1 2>/dev/null; for b in $(git branch --list 'wave1/*'); do git branch -D "$b" 2>/dev/null; done
rm -rf output/

# Verify
docker images | grep biokea-binner-base | wc -l   # → 20
ls .claude/skills/integrate-binner/SKILL.md       # → exists
ls data/strong100/assembly.fasta                   # → OK
```

Kill any stale claude processes from earlier botched dispatch:
```bash
pkill -f 'claude -p' 2>&1; pkill -f 'dispatch_wave' 2>&1
```

---

## 1. Window setup

**Just one window.** A wide terminal running Claude Code in chat mode, in the repo directory.

```bash
cd /Users/seanjungbluth/Desktop/binner-fleets-demo
claude
```

You'll be at the chat prompt. Make the terminal large — when you `/agents` to peek, the table view fills the screen.

### Recording

`Cmd+Shift+5` → Record Selected Portion → drag a box covering the terminal. Audio on for VO. Save to `~/Desktop/binner-fleets-demo-take2.mov`.

---

## 2. The take — 4 prompts you read on camera

**Time-lapse all wait phases in editing.** Total real wall-clock: ~60–90 min.

### Beat 1 — Cold open (~15 s)
- Camera on. You're at the empty Claude chat prompt.
- Voiceover: *"This is BioKEA's binner-fleets-demo. We're about to integrate 16 metagenome binners in parallel by asking Claude to fan out 16 sub-agents from this single chat. Watch."*
- Type `/agents`. Confirm "Running" tab is empty. Esc.

### Beat 2 — Wave 1 prompt (~15 s to type)

Type this prompt in the chat (paste the whole block — multi-line is fine):

```
I need to integrate 16 metagenome binners into BioKEA's binner-fleets-demo
repo. Use the integrate-binner skill at .claude/skills/integrate-binner/SKILL.md
for each. Dispatch sub-agents in two batches of 8, in parallel within each
batch, to avoid saturating Docker on the host:

BATCH 1 (dispatch first, in parallel):
  metabat2, concoct, maxbin2, vamb, semibin2, comebin, genomeface, taxvamb

BATCH 2 (dispatch after BATCH 1's 8 sub-agents complete, in parallel):
  metabinner, metadecoder, graphbin2, metacoag, graphmb, unitigbin, mycc, cocacola

For each tool, the sub-agent should:
1. Read tools/<tool>/spec.yaml
2. docker build using the existing docker/<tool>/Dockerfile (most images are
   already cached locally as biokea-binner-base:1.0-<tool>)
3. Smoke-test on data/5G_metaSPAdes/
4. Run on data/strong100/
5. Parse output to BinSet (biokea/schema.py) and write to
   output/wave1/<tool>/bins.parquet
6. Write biokea/binners/<tool>.py adapter (~50 LOC implementing BinnerAdapter)
7. Commit to a wave1/<tool> sub-branch

vamb and taxvamb will fail with a pycoverm/Rust error — when that happens,
those sub-agents will report the failure. I'll provide the unblock fix
inline at that point. Begin.
```

Hit Enter.

### Beat 3 — Watch the fan-out (~5 s after Enter)
- Claude will respond with a brief plan, then start dispatching sub-agents (you'll see Task tool calls in the chat output).
- Type `/agents` (use Tab/Esc tactically — see below).
- The "Running" tab fills with 8 sub-agents (Batch 1) within ~3 seconds.
- Color-coded states. **This is the hero shot.**
- Esc to return to chat.

### Beat 4 — Quiet shepherding (~15–20 min for Batch 1)
- While Batch 1 runs, periodically `/agents` to peek at the table.
- Cached-image tools (metabat2, concoct, maxbin2, semibin2, comebin, genomeface) finish in ~30–90 s.
- vamb and taxvamb will block. **Stay calm.** When they report failure (Claude will surface in chat), continue to Beat 5.

### Beat 5 — Vamb unblock (~5 min real-time)
When Claude reports vamb failed (pycoverm metadata-generation), reply in chat:

```
For vamb: replace docker/vamb/Dockerfile with this content, then rebuild
the image and re-run the integrate-binner skill:

FROM biokea-binner-base:1.0
USER root
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable && . "$HOME/.cargo/env"
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install --no-cache-dir maturin
RUN pip install --no-cache-dir vamb
WORKDIR /work

Apply the same pattern to taxvamb (last line: pip install "vamb>=5"). Both
should work after the rebuild.
```

Claude's sub-agent for vamb (and taxvamb) re-runs the steps, this time succeeding. ~5 min for Rust/pycoverm to compile.

### Beat 6 — Batch 2 dispatch (~automatic)
- Claude noticed Batch 1 completed; it auto-dispatches Batch 2.
- `/agents` shows the next 8 sub-agents.
- mostly clean (all cached images at this point); ~5–10 min.

### Beat 7 — Wave 1 done (~30 s)
When all 16 are done, prompt:

```
Wave 1 complete? Run scripts/finalize_wave1.sh to merge all wave1/<tool>
sub-branches into the wave1 branch in deterministic order. Then verify
output/wave1/*/bins.parquet count is 16.
```

Claude runs the script. ~30 sec.

### Beat 8 — Wave 2 (~5–15 min)
Prompt:

```
Now Wave 2 — the 4 refiners. Dispatch 4 sub-agents in parallel for:
das_tool, metawrap, magscot, binette. Each reads the unified Wave 1 output
(output/wave1/*/bins.parquet) and produces refined bins at
output/wave2/<refiner>/bins.parquet. Use the integrate-binner skill.
```

Show /agents twice during this — once when sub-agents appear, once when they're nearly done.

### Beat 9 — Wave 3 (~30 s)
Prompt:

```
Now Wave 3 — biokea's v0 ensembler. Run scripts/dispatch_wave3.sh. This
runs biokea/ensemble.py against the Wave 1 output and produces
output/wave3/biokea-v0/bins.parquet.
```

### Beat 10 — Score reveal (~1 min, THE CLOSING SHOT)
Prompt:

```
Final step — score the leaderboard. Run .venv/bin/python scripts/score.py
and open output/score/leaderboard.png.
```

When the leaderboard appears, narrate based on biokea-v0's position:
- **On top of all 4 refiners**: *"biokea v0 leads. This is our starting point."*
- **Competitive (within ~10% of best refiner)**: *"biokea v0 is competitive with state-of-the-art. The roadmap takes it from here."*
- **Below all 4 refiners**: *"biokea v0 is the seed. Here's the field — every result you see came from one afternoon of integration."*

### Beat 11 — Final flourish (~15 s)
Prompt:

```
Merge wave1 into main and show the final repo state. Then we're done.
```

Claude shows the merge + git log. Cut.

---

## 3. Post-record

```bash
mv ~/Desktop/binner-fleets-demo-take2.mov ~/Desktop/binner-fleets-demo-take2-$(date +%Y%m%d-%H%M).mov
ls output/score/leaderboard.{png,json}
git status
git push origin main
```

---

## 4. Recovery if things go sideways

| Symptom | What to do |
|---|---|
| `/agents` Running stays empty after the prompt | Claude isn't dispatching sub-agents. Re-prompt: "Please use your Task tool to dispatch one sub-agent per binner — I want to see them in /agents Running." |
| A sub-agent in Batch 1 fails on something other than vamb/taxvamb | Reply in chat: "What's the error?" Claude reports. Most likely a CLI flag mismatch or missing data path — paste a corrected invocation in chat, sub-agent re-runs. |
| Mac CPU/memory saturates badly | Pause: tell Claude "stop dispatching new sub-agents until current batch finishes." |
| biokea v0 collapses on leaderboard | Use the honest-fallback narration. Don't fudge numbers. |
| You drift off-script | The prompts above are checkpoints, not exact incantations. Improvise within the same flow: dispatch → watch → score. |

---

## 5. Cheat-sheet (single screen, print this)

```
WINDOW: claude  (in /Users/seanjungbluth/Desktop/binner-fleets-demo)

Slash commands:
  /agents    → switch to ←/→ "Running" tab, see sub-agents live
  Esc        → close /agents back to chat

The 4 prompts (in order):
  1. Wave 1: integrate 16 binners in 2 batches of 8 (~30 min)
  2. Vamb + taxvamb unblock fix (~5 min)
  3. Wave 2: 4 refiners (~10 min)
  4. Wave 3: biokea v0 + score reveal (~2 min)

VAMB / TAXVAMB UNBLOCK FIX (paste when they fail):
  Replace Dockerfile with:
    FROM biokea-binner-base:1.0
    USER root
    RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable && . "$HOME/.cargo/env"
    ENV PATH="/root/.cargo/bin:${PATH}"
    RUN pip install --no-cache-dir maturin
    RUN pip install --no-cache-dir vamb        ← (taxvamb: "vamb>=5")
    WORKDIR /work
```
