# binner-fleets-demo

A demo of [Claude Fleets EAP](https://platform.claude.com/docs/en/managed-agents/overview): 20 metagenome binners integrated in parallel, scored on STRONG100 ground truth, surfaced through one ensembler.

## What this is

- **Wave 1**: 16 primary binners (MetaBAT2, CONCOCT, MaxBin2, VAMB, SemiBin2, COMEBin, GenomeFace, TaxVAMB, MetaBinner, MetaDecoder, GraphBin2, MetaCoAG, GraphMB, UnitigBIN, MyCC, COCACOLA), each integrated by a parallel Claude Fleets session.
- **Wave 2**: 4 refiners (DAS_Tool, MetaWRAP, MAGScoT, Binette) consuming Wave 1's unified bin output.
- **Wave 3**: biokea v0 ensembler consuming the same Wave 1 inputs.
- **Scoring**: AMBER against STRONG100 ground truth.

## Reproduce

```bash
git clone https://github.com/BioKEA/binner-fleets-demo
cd binner-fleets-demo
bash scripts/run_demo.sh
```

(Requires Docker and a Claude Code installation with Fleets EAP access.)

## Layout

See `docs/runbook.md` for the full pre-flight and recording-day procedure.

## License

Apache 2.0.
