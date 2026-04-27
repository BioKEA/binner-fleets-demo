# Recording Day Runbook — Binner Fleets Demo

This is the operator's hands-on script for recording the demo. The canary dry-run **is** the take — no rehearsal.

---

## 0. Pre-record checklist (do once, off-camera)

```bash
cd /Users/seanjungbluth/Desktop/binner-fleets-demo

# Verify clean state
git status                                    # → clean
git pull --ff-only                            # → up to date
git branch -D wave1 wave1/* 2>/dev/null || true   # delete any stale local branches
rm -rf output/                                 # clean prior run artifacts

# Verify Docker images
docker images | grep biokea-binner-base | wc -l   # → 20

# Verify data
ls data/strong100/assembly.fasta data/strong100/assembly_graph.gfa
ls data/5G_metaSPAdes/

# Verify skill discoverable (single test dispatch — kill before recording)
claude --bg "echo skill_discovery_test"
claude agents              # confirm the test session appears
# In claude agents UI: select that session, press 'k' or whatever your build uses to kill it.
# If unclear: just let it expire; the test session will mark done in seconds.
```

If all green: proceed.

---

## 1. Two-window setup

### Window 1 — DISPATCHER (left or top, ~40% of screen)
- A regular terminal (Ghostty / iTerm / Terminal).
- `cd /Users/seanjungbluth/Desktop/binner-fleets-demo`
- This is where you run the dispatch scripts: `dispatch_wave1.sh`, `dispatch_wave2.sh`, `dispatch_wave3.sh`, `score.py`.
- Also where you peek-and-reply unblocks (in this build, peeks may land here or in Window 2 depending on the EAP build).

### Window 2 — `claude agents` HERO (right or bottom, ~60% of screen)
- A Claude Code terminal session.
- `cd /Users/seanjungbluth/Desktop/binner-fleets-demo` (so it picks up `.claude/skills/`).
- Run `claude` to enter Claude Code, then `claude agents` (or whatever the EAP build's command is — the PDF says `claude agents`).
- This is the table view, the hero shot. Color-coded session states, `space`-to-peek, `enter`-to-attach.

### Recording
- Easiest on macOS without OBS: **Cmd+Shift+5 → Record selected portion → drag a box that covers BOTH windows**. Click "Record" right before you start dispatch.
- Audio: enable mic if you want voiceover, disable if you'll add VO post.
- Backup: in a third terminal, `script -q /tmp/binner-fleets-recording.cast` to text-capture commands as failover.
- Save location: `~/Desktop/binner-fleets-demo-take1.mov` (date-stamp manually after).

If you do have OBS: install with `brew install --cask obs`; configure a single scene with display capture; start record there instead.

---

## 2. Recording sequence (the take)

**Total wall-clock estimate: 50–90 minutes.** Time-lapsed in editing.

### Beat 1 — Cold open (~25s)
```
[Window 2]  claude agents
```
- Empty table appears. Voiceover or written caption: *"This is Claude Fleets. We're about to integrate 16 metagenome binners in parallel."*

### Beat 2 — Dispatch Wave 1 (~30s)
```
[Window 1]  bash scripts/dispatch_wave1.sh
```
- 16 sessions appear in Window 2's table within ~3 seconds, all yellow/working.

### Beat 3 — Reading the table (~20s)
- Narrate the columns: state icon (color), session id, one-line summary.
- Color overlay caption (post-edit): "🟡 working   🟢 done   🟠 blocked   🔴 failed"

### Beat 4 — Quiet shepherding (~15–20 min — TIME-LAPSE in edit)
- Sessions start completing. Greens trickle in. Most cached-image tools (metabat2, concoct, etc.) finish in ~30–90s. Heavier ones (comebin, graphmb) take 5–10 min.
- Counter overlay (post-edit): `n done / n blocked / n working`.

### Beat 5 — First planned-block: VAMB (~3–5 min real-time)
When `vamb` goes 🟠 (amber):
1. **Window 2:** select the vamb session, press `space` to peek.
2. Read the error in the peek panel. It says something like `pycoverm metadata-generation-failed`.
3. Reply (paste from `docs/install-postmortems.md` Planned-block #1 — the ~7-line Dockerfile replacement):

```
Replace docker/vamb/Dockerfile with this content, then rebuild:

FROM biokea-binner-base:1.0
USER root
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable \
    && . "$HOME/.cargo/env"
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install --no-cache-dir maturin
RUN pip install --no-cache-dir vamb
WORKDIR /work
```

4. Send the reply. Peek closes; vamb session goes back to 🟡 working.
5. Vamb's Fleet agent edits the Dockerfile, rebuilds, smoke-tests, runs on STRONG100. ~5 min.

### Beat 6 — Second planned-block: TAXVAMB (~3–5 min real-time)
Same pattern as vamb. Paste from postmortem Planned-block #2:

```
Replace docker/taxvamb/Dockerfile with this content, then rebuild:

FROM biokea-binner-base:1.0
USER root
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable \
    && . "$HOME/.cargo/env"
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install --no-cache-dir maturin
RUN pip install --no-cache-dir "vamb>=5"
WORKDIR /work
```

Optional narration: *"Same fix as vamb — taxvamb shares the pycoverm dep."*

### Beat 7 — One full attach (~30s)
- For variety: pick any session that's still 🟡 working (e.g., comebin or graphmb).
- Press `enter` to attach to its full transcript.
- Show ~10 lines of the binner's actual run output (parsing GFA, k-mer count, etc.).
- Press `escape` (or whatever detaches) to return to the table.
- Caption: *"Sometimes you want the full transcript. `enter` attaches, `escape` returns."*

### Beat 8 — Cross-platform B-roll (~15–20s, optional)
- Open Web view (`https://claude.com/code` or wherever the Fleets web UI lives).
- Show the SAME 16 sessions in the browser. Then phone if you have remote-control on (per spec D14).
- Caption: *"Same fleet, anywhere."*
- Cut back to terminal.

### Beat 9 — Wave 1 complete (~30s)
When all 16 are 🟢:
```
[Window 1]  ls output/wave1/*/bins.parquet | wc -l    # → 16
            bash scripts/finalize_wave1.sh
```
- Output shows sub-branches merging into `wave1` in deterministic order.
- Caption: *"16 binners → 16 parquet files → one branch."*

### Beat 10 — Dispatch Wave 2 (~1 min, then 5–15 min wait)
```
[Window 1]  bash scripts/dispatch_wave2.sh
```
- 4 refiner sessions appear in Window 2's table.
- Caption: *"Wave 2: 4 refiners reading Wave 1's unified output."*
- Wait for all 4 to go 🟢. Time-lapse in edit.

### Beat 11 — Wave 3: biokea v0 (~30s)
```
[Window 1]  bash scripts/dispatch_wave3.sh
```
- Single line: `biokea-v0 produced N bins from M contig assignments`.
- Caption: *"Wave 3: biokea's ensembler runs on the same Wave 1 inputs."*

### Beat 12 — Score reveal (~1 min — THE CLOSING SHOT)
```
[Window 1]  .venv/bin/python scripts/score.py
            open output/score/leaderboard.png
```
- Leaderboard PNG opens. biokea-v0 highlighted in red.
- **If biokea-v0 is on top of the 4 refiners**: caption *"biokea v0 leads the field. This is our starting point."*
- **If biokea-v0 is competitive (within ~10% of best refiner)**: caption *"biokea v0 is competitive with state-of-the-art refiners — and there's a roadmap from here."* (the spec's pre-committed honest-fallback wording)
- **If biokea-v0 is well behind**: caption *"biokea v0 is the seed. Here's the field we're competing with — every result you see here came from one afternoon of integration."*

### Beat 13 — Final flourish (~15s)
```
[Window 1]  git -C . merge wave1 --ff-only main
            git push origin main
            git log --oneline | head -25
```
- Show the commit history filling up. ~17 binner adapter commits + biokea v0.
- Cut to fade.

---

## 3. Post-record (off-camera)

```bash
# Stop OBS / Cmd+Shift+5 recording
# Stop the script(1) backup if running

# Move artifacts
mv ~/Desktop/binner-fleets-demo-take1.mov ~/Desktop/binner-fleets-demo-take1-$(date +%Y%m%d-%H%M).mov
cp /tmp/binner-fleets-recording.cast ~/Desktop/  # backup transcript

# Verify the leaderboard exists
ls -la output/score/leaderboard.{png,json}

# Final commit + push
git status
git add -A
git commit -m "demo: complete take 1 (all 21 sessions + leaderboard)"
git push origin main
```

---

## 4. Recovery branches (if something goes sideways)

| Symptom | What to do |
|---|---|
| Wave 1 session that should be cached goes amber on a different error | Peek; if it's a CLI flag mismatch (e.g., metabat2 wants `-i` not `--input`), reply with the correct invocation. The Fleet agent retries. |
| Skill not discovered (Wave 1 sessions never appear) | Stop recording. Verify `.claude/skills/integrate-binner/SKILL.md` exists; restart `claude` from the repo dir. Re-take. |
| OBS / screen-record crashes mid-take | Keep going — `script` backup captures terminal text. You can re-shoot the visual portions later. |
| biokea v0 leaderboard collapses | Use the honest-fallback narration. Don't pretend a number is something it isn't. |
| Multiple sessions blocked simultaneously you don't expect | Peek the first one, paste a guess fix. If it's a category (e.g., another conda channel issue) the same fix applies to siblings. |
| You lose your place in the runbook | Window 1 has the runbook open in your editor. Switch focus, find your beat, resume. |

---

## 5. Cheat-sheet (single screen, print this)

```
WINDOW 1 (DISPATCHER)
  bash scripts/dispatch_wave1.sh
  # wait for all 16 done
  bash scripts/finalize_wave1.sh
  bash scripts/dispatch_wave2.sh
  # wait for all 4 done
  bash scripts/dispatch_wave3.sh
  .venv/bin/python scripts/score.py
  open output/score/leaderboard.png

WINDOW 2 (claude agents)
  claude agents
  space    → peek session
  enter    → attach to session
  escape   → detach back to table

PLANNED-BLOCK FIXES (paste from docs/install-postmortems.md):
  vamb     → rustup + maturin + pip install vamb
  taxvamb  → rustup + maturin + pip install "vamb>=5"
```
