# EFMW-inspired CFSG rebuild optimization note

**Status:** design and source-level feasibility review only. No complete CFSG rebuild has been run here.

## What was measured

- The present ChatGPT execution container has 5 CPU cores, approximately 5.8 GiB RAM, 30 GiB of free disk, and no installed Lean or Lake toolchain.
- The repository's pinned lakefile declares **127 default targets**.
- CFSG.lean directly imports approximately **1,766** modules, so compilation may involve an extensive transitive dependency graph.
- Frozen proof target: `69cb972f587a3ecc035e092253167ff2e303c962`.
- The existing GitHub hosted source-preflight run succeeded, but did **not** compile the theorem.

## Optimize without changing mathematical trust

1. Retain the exact frozen Lean, Mathlib and TauCeti pins.
2. Use Lake's built-in incremental build graph; reuse only artifacts tied to exact inputs.
3. Optionally compile the `Comparator` target ahead of the 127-target project-wide build to locate critical-path issues early. This may improve *time to first meaningful failure* but does not necessarily improve the total successful-build time.
4. Collect time, peak resident memory, free disk and build-stage diagnostics from the external runner.
5. Use conservative EWMA smoothing or an EFMW-inspired recurrent monitor to *flag* stalls and memory exhaustion. This is an operational heuristic, **not** a proven EFMW compiler speed-up. Never use it to skip Lean kernel checks.
6. After the complete build, run `audit/CFSGChainCheck.lean`, verify actual printed axioms, and retain logs.
7. Keep full Zoo animal execution separate from the Lean rebuild.

## Compute boundary

The ChatGPT Astra reasoning model is not a dedicated 64-GB, day-long Lean build machine. This chat container cannot finish this workload with its current capacity; a runner with sufficient RAM, disk, and time is required. ChatGPT can still analyze source, prepare build scripts and compare logs. Do not mark a proof verified from monitoring output, a source-level check, or a simulated build.

## Links

- [Full rebuild workflow](../.github/workflows/cfsg-full-rebuild.yml)
- [Reconstruction plan](CFSG_REBUILD_PLAN.md)
- [Source preflight](../scripts/verify_cfsg_source.py)
- [Final axiom probe](CFSGChainCheck.lean)
- [Lake documentation](https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/)
