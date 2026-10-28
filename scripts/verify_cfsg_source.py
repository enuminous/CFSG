#!/usr/bin/env python3
"""Frozen CFSG source preflight, not a Lean compilation or a Zoo-kernel execution."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "69cb972f587a3ecc035e092253167ff2e303c962"
MATHLIB = "b63f6e8a68d220e3b3bc4f3792bb53650d375f24"
TAUCETI = "6e0c6acab5f4c6f42e5f5bab9bd5e4e84f74c380"
TOOLCHAIN = "leanprover/lean4:v4.35.0-rc3"
PROOF_PATHS = [
    "CFSG", "Certificates", "Comparator", "CFSG.lean",
    "CFSGWithCertificates.lean", "CertifiedResults.lean",
    "CertifiedMilestones.lean", "CertifiedYardstones.lean",
    "YardstoneContract.lean", "lakefile.toml",
    "lake-manifest.json", "lean-toolchain", "formalization.yaml",
    "comparator.json",
]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def git(*args: str):
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False
    )

def run_check() -> dict:
    checks = []
    def check(name: str, ok: bool, details: str):
        checks.append({"name": name, "status": "PASS" if ok else "FAIL", "details": details})

    try:
        tc = read("lean-toolchain").strip()
        manifest = json.loads(read("lake-manifest.json"))
        comparator_cfg = json.loads(read("comparator.json"))
        sol = read("Comparator/Solution.lean")
        chal = read("Comparator/Challenge.lean")
        stat = read("CFSG/Statement.lean")
        certified = read("CFSG/Certified/Classification.lean")
        milestone = read("CFSG/Milestones/CFSG_classification.lean")
        meta = read("formalization.yaml")
        axiom_file = read("audit/CFSGChainCheck.lean")
    except (OSError, ValueError, json.JSONDecodeError) as ex:
        return {"status": "FAIL", "error": f"Missing or invalid required input: {ex}", "checks": []}

    check("lean_toolchain", tc == TOOLCHAIN, tc)
    pkgs = {p.get("name"): p.get("rev") for p in manifest.get("packages", [])}
    check("mathlib_pin", pkgs.get("mathlib") == MATHLIB, str(pkgs.get("mathlib")))
    check("tauceti_pin", pkgs.get("TauCeti") == TAUCETI, str(pkgs.get("TauCeti")))
    check("comparator_goal", "theorem CFSGComparator.classification : TauCeti.ClassificationStatement" in sol,
          "Submitted comparator theorem has TauCeti classification target")
    check("solution_has_no_literal_sorry", "sorry" not in sol,
          "Only scans Comparator/Solution.lean, NOT its transitive imports")
    check("challenge_is_separate", "sorry" in chal and "theorem CFSGComparator.classification" in chal,
          "Challenge is a template, not the submitted proof")
    check("certified_bridge", "CFSG.Certified.classification_finite_simple_groups" in sol and
          "CFSG.classification_finite_simple_groups" in certified,
          "Submitted comparator -> certified wrapper -> CFSG theorem")
    check("assembled_theorem", "Assembly.classification Assembly.InCatalog" in stat,
          "The theorem body references the classification assembly")
    check("native_milestone_present", "theorem cfsg_classification_native_and_realization :" in milestone,
          "A second substantive final theorem is defined")
    check("declared_axioms", set(comparator_cfg.get("permitted_axioms", [])) ==
          {"propext", "Quot.sound", "Classical.choice"},
          "Only validates a JSON *declaration*, not the actual theorem axioms")
    check("self_assessed_review", "status: self-assessed" in meta,
          "The source metadata labels its review self-assessed")
    check("axiom_probe_has_targets",
          "#print axioms CFSGComparator.classification" in axiom_file and
          "#print axioms CFSG.Milestones.cfsg_classification_native_and_realization" in axiom_file,
          "Probe file targets the two declared final theorems")

    ancestor = git("merge-base", "--is-ancestor", BASE, "HEAD")
    check("frozen_commit_ancestor", ancestor.returncode == 0,
          "Original Axiom Math snapshot is part of this fork's checked-out history")
    if ancestor.returncode == 0:
        diff = git("diff", "--quiet", BASE, "HEAD", "--", *PROOF_PATHS)
        check("proof_source_unmodified", diff.returncode == 0,
              "Protected proof paths and dependency manifests match the initial commit" if
              diff.returncode == 0 else "Proof source, pins, or declarations changed since frozen commit")
    else:
        check("proof_source_unmodified", False,
              "Cannot establish unchanged proof paths without original commit")

    return {
        "schema_version": 1,
        "kind": "cfsg_source_preflight",
        "frozen_base": BASE,
        "head": git("rev-parse", "HEAD").stdout.strip(),
        "status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
        "scope": "Selected source text and commit/provenance checks only; DOES NOT run Lean or a full Zoo audit.",
        "checks": checks
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", default="audit/cfsg-preflight-result.json")
    args = p.parse_args()
    out = run_check()
    dest = ROOT / args.report
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "report": str(dest),
        "passed": sum(c["status"] == "PASS" for c in out["checks"]),
        "failed": sum(c["status"] == "FAIL" for c in out["checks"]),
        "reason": out.get("error")
    }))
    sys.exit(0 if out["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
