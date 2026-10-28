# CFSG complete proof-chain reconstruction — reproducibility plan

**Status as of 28 October 2026:** **SOURCE PREFLIGHT PASSED; FULL LEAN REBUILD NOT YET EXECUTED BY THIS AUDIT.**

The reconstructed target is the original mathematical work published by the Axiom Math / CFSG contributors. This fork's verification instrumentation does not claim ownership of the original proof. See [formalization.yaml](../formalization.yaml) for original author and contributor attribution.

## Frozen target

- **Original proof commit:** [`69cb972f587a3ecc035e092253167ff2e303c962`](https://github.com/enuminous/CFSG/commit/69cb972f587a3ecc035e092253167ff2e303c962).
- **Lean toolchain:** `leanprover/lean4:v4.35.0-rc3`.
- **Mathlib:** `b63f6e8a68d220e3b3bc4f3792bb53650d375f24`.
- **TauCeti:** `6e0c6acab5f4c6f42e5f5bab9bd5e4e84f74c380`.
- **Classification theorem:** `CFSGComparator.classification : TauCeti.ClassificationStatement` in [Comparator/Solution.lean](../Comparator/Solution.lean).
- **Internal classification theorem:** `CFSG.classification_finite_simple_groups` in [CFSG/Statement.lean](../CFSG/Statement.lean), via [CFSG/Certified/Classification.lean](../CFSG/Certified/Classification.lean).
- **Independent concluding milestone to inspect:** `CFSG.Milestones.cfsg_classification_native_and_realization` in [CFSG/Milestones/CFSG_classification.lean](../CFSG/Milestones/CFSG_classification.lean).

The source preflight checks that the original proof, manifests, and trust-sensitive files have not changed since the initial commit. It is intentionally strict; revisions require a new freeze and review record rather than silently inheriting an earlier verification.

## Build phases and evidence

| Phase | Command / artifact | Current status |
|---|---|---|
| 0. Confirm original proofs and pins | `python3 scripts/verify_cfsg_source.py` | **PASS: 14/14** in [hosted preflight](https://github.com/enuminous/CFSG/actions/runs/40733464376) |
| 1. Verify parser and rebuild script syntax | Five parser unit tests plus `bash -n scripts/rebuild_cfsg_full.sh` | **PASS: 5/5 tests and shell lint** in [hosted preflight](https://github.com/enuminous/CFSG/actions/runs/40733464376) |
| 2. Clean source checkout & toolchain | `git clone`, `lake --version`, `lean --version` | NOT YET REPRODUCED for full source |
| 3. Complete project compilation | `lake build -j 4` | **UNRESOLVED — not executed here** |
| 4. Two final theorem axiom reports | `lake env lean audit/CFSGChainCheck.lean` | **UNRESOLVED — requires complete build** |
| 5. Machine check of printed axiom lists | `python3 scripts/verify_cfsg_axioms.py --log ...` | **UNRESOLVED — awaits actual Lean output** |
| 6. Independent certificate-closure review | Check all reachable dependencies / theorem semantics | **UNRESOLVED** |
| 7. Forty-six Zoo animal operations | Run registered animal-specific auditors with evidence | **UNRESOLVED; do not conflate with this rebuild** |

The [previous static Zoo audit](CFSG_ZOO_2026-10-27.md) has 10 bounded static passes, 3 larger unresolved checks and 46 **UNRESOLVED** animal results. It is **not** a failing CFSG theorem proof. A `sorry` in [Comparator/Challenge.lean](../Comparator/Challenge.lean) is a *template* and must not be mistaken for a hole in the submitted [Comparator/Solution.lean](../Comparator/Solution.lean).

## Complete rebuild on an adequate Linux runner

This repository is reported by GitHub at roughly 6 GB of source (repository size metadata `6071207` KB). Upstream says its full build needed optimizations or in-progress Lake changes to finish in under 24 hours. **The exact hardware capacity and upstream Lake patch requirements have not yet been independently verified**.

A reasonable *starting allocation*, not a demonstrated minimum, is a Linux x64 machine with **at least 64 GB RAM, 150–200 GB free disk, several CPU cores, and the ability to run for 24 hours or more**. Memory, disk or timeout failures must be classified as infrastructure failures, not mathematical contradictions.

Make the runner a trusted, isolated machine, since it will build a large third-party project. Install Git, Python 3, elan, a working C/C++ toolchain and standard Linux utilities (including GNU `timeout`). Ensure the toolchain in `lean-toolchain` is installed and used. If non-upstream Lake modifications are genuinely required, document their exact source SHA and patch and rerun preflight under a **new** environment lock; do not silently change the pinned proof.

For a clean clone:

```bash
git clone https://github.com/enuminous/CFSG.git
cd CFSG
git status --porcelain
cat lean-toolchain
python3 -m unittest discover -s scripts -p 'test_verify_cfsg_axioms.py' -v
python3 scripts/verify_cfsg_source.py --report audit-results/source-preflight.json
CFSG_JOBS=4 CFSG_BUILD_TIMEOUT=20h bash scripts/rebuild_cfsg_full.sh
```

The script runs `lake build` for the entire project, captures stdout/stderr, then imports the final theorems in [CFSGChainCheck.lean](CFSGChainCheck.lean) and prints their axioms using Lean. The strict log parser accepts exactly these names (or a subset): `propext`, `Quot.sound`, `Classical.choice`. An absent log, malformed output, extra axiom such as `sorryAx`, a compiler failure, or an incomplete source pin produces a non-pass.

**GitHub Actions:** A [full-rebuild workflow](https://github.com/enuminous/CFSG/actions/workflows/cfsg-full-rebuild.yml) is defined with a manual dispatch trigger. It requests runner labels `self-hosted`, `linux`, `x64`, `cfsg-large`. **No such runner has been verified as connected.** The workflow does not run on GitHub's ordinary 14-GB / six-hour hosted runner. Its evidence log uploads only after a runner accepts the job. Its existence is not a report of a completed rebuild.

## Interpretation and trust boundary

A successful `lake build` is valuable but not the entire audit. The final theorem's *actual* `#print axioms` output must be stored, along with pinned toolchain hashes, full build logs, and statement equivalence evidence.

In particular:

1. A theorem with no literal `sorry` in its immediate source can depend transitively on unverified axioms.
2. `#print axioms` checks the names of axioms associated with a declaration as Lean sees it, not the informal correctness of the classification predicate.
3. A formally proved restatement of a weaker condition is not automatically the historical CFSG; this implementation uses the TauCeti statement and requires independent statement-alignment review.
4. Certificate generation, native computations and trusted primitive evaluation need specific provenance and exact verification.
5. The original proof claims remain those of the Axiom Math team and its contributors.

## Acceptance definition

Mark **COMPLETE — REPRODUCED** *only* after the entire pinned source is built from a fresh checkout with recorded environment and no unreviewed proof-source changes; both final target theorem axiom checks pass; output logs and artifact checksums are retained; the full dependency and certificate closure is independently inspected; and the theorem statement is confirmed against the intended TauCeti and CFSG semantics.

Before then the correct overall status is **UNRESOLVED / REBUILD IN PROGRESS**, regardless of partial preflight passes. No claim of completed proof reconstruction is made by this document.

**Evidence locations:** `audit-results/cfsg-rebuild/` on a rebuild host; hosted CI artifacts on the specific GitHub Actions run. The scripts intentionally do not commit logs into the source tree.
