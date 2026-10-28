# Classification of Finite Simple Groups in Lean
* [Website](https://cfsg.axiommath.ai/)

<!-- MONOLITHIC-CFSG-AUDIT-NAV:START -->
## Navigation and independent evidence review

**Repository map:** [Main claim](#classification-of-finite-simple-groups-in-lean) · [Proof entry points](#proof-entry-points) · [Checking the proof](#checking-the-proof) · [Monolithic Zoo review](#monolithic-zoo-audit-27-october-2026) · [License](#license)

**Source evidence:** [Comparator solution](Comparator/Solution.lean) · [CFSG main statement](CFSG/Statement.lean) · [Certified classification wrapper](CFSG/Certified/Classification.lean) · [Native realization milestone](CFSG/Milestones/CFSG_classification.lean) · [Toolchain](lean-toolchain) · [Lake manifest](lake-manifest.json) · [Formalization metadata](formalization.yaml).

**Related research:** [TauCeti project](https://github.com/TauCetiProject/TauCeti) · [Mathlib](https://github.com/leanprover-community/mathlib4) · [Monolithic Zoo](https://github.com/enuminous/Monolithic-Zoo-Lean4) · [eNuminous audit index](https://github.com/enuminous/EFMW_Post156_Zoo_Audit).

### Proof entry points

- `Comparator/Solution.lean` states `CFSGComparator.classification : TauCeti.ClassificationStatement`, referring to `CFSG.Certified.classification_finite_simple_groups`.
- `CFSG/Certified/Classification.lean` exposes a wrapper around the theorem in `CFSG/Statement.lean`.
- `CFSG/Statement.lean` assembles its conclusion from named finite-group classification results.
- `Comparator/Challenge.lean` is a separate **challenge template** that contains `sorry`. This does not establish a hole in the submitted solution.

### Monolithic Zoo audit — 27 October 2026

**[Read the full bounded CFSG Zoo audit](audit/CFSG_ZOO_2026-10-27.md)** · **[Machine-readable 46-animal evidence intake](audit/CFSG_ZOO_INTAKE_2026-10-27.json)**

The audit examines the repository's pinned initial commit, `69cb972f587a3ecc035e092253167ff2e303c962`. **Ten static source-inspection checks passed** (e.g. source-level proof path and pinned dependencies), while three larger proof-verification questions remained unresolved. **The 46 Zoo animal operations were not executed**: all 46 intake statuses are `UNRESOLVED`, so the alternative Zoo evidence limiter returns `QUALIFIED`, not `ESTABLISHED`.

A successful independent `lake build`, exact `#print axioms` outputs and full transitive certificate/import inspection remain required to confirm the repository's sorry-free, standard-axiom claims. The audit does **not** refute CFSG or claim that the original source's authors were Monolithic or EFMW contributors.

<!-- MONOLITHIC-CFSG-AUDIT-NAV:END -->


A sorry-free Lean4 (v4.35.0-rc3) proof of the Classification of Finite Simple Groups (CFSG), built on Mathlib and TauCeti, using the standard axioms `Classical.choice`, `propext`, and `Quot.sound` (no `native_decide`). We primarily follow the first generation proof of CFSG.

We use the [statement of CFSG from the TauCeti project](https://github.com/TauCetiProject/TauCeti/blob/6e0c6acab5f4c6f42e5f5bab9bd5e4e84f74c380/TauCeti/GroupTheory/SpecificGroups/CFSG/Classification.lean#L52-L56)

```lean4
/-- **Classification of finite simple groups, statement only.** Every finite simple group is
isomorphic to one of the explicitly constructed groups on the classification list. -/
def ClassificationStatement : Prop :=
  ∀ (G : Type u) [Group G] [Finite G] [IsSimpleGroup G],
    ∃ i : CFSGIndex, Nonempty (G ≃* i.Group)
```

## Checking the proof

`lake build` builds the entire project. We used a few open changes to Lake and some optimizations we plan to upstream soon to get this project's build time under 24 hours.

## Full-chain reconstruction in this fork

The [complete reconstruction plan](audit/CFSG_REBUILD_PLAN.md) specifies a clean rebuild of the **entire** CFSG import and certificate chain, followed by Lean axiom checks on both the comparator and native realization theorem. The original mathematical source files and dependency pins are kept at the initial Axiom Math commit `69cb972f587a3ecc035e092253167ff2e303c962`.

**Verification status:** [source-provenance preflight PASS — 14/14 checks, 5/5 parser tests, shell syntax](https://github.com/enuminous/CFSG/actions/runs/40733464376). **Full `lake build`: not yet independently reproduced in this fork.** The large build requires a capable Linux machine; see the [manually dispatchable full-rebuild workflow](https://github.com/enuminous/CFSG/actions/workflows/cfsg-full-rebuild.yml), which requires an appropriately labeled self-hosted runner.

**[EFMW-inspired rebuild optimization and Astra execution limits](audit/EFMW_CFSG_OPTIMIZATION_NOTE.md)** — a source-level optimization plan, not a complete proof run.

The checked-in verification entry points are [source preflight](scripts/verify_cfsg_source.py), [full rebuild](scripts/rebuild_cfsg_full.sh), [Lean final-axiom probe](audit/CFSGChainCheck.lean), [axiom-output checker](scripts/verify_cfsg_axioms.py), and [parser regression tests](scripts/test_verify_cfsg_axioms.py). These constitute a reproducibility *harness*, not a new proof or an executed 46-animal Zoo pass.

# License

APACHE-2.0
