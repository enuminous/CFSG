#!/usr/bin/env python3
"""Read Lean axiom output for the two final CFSG declarations.

This checks textual Lean output from a completed build; it does not itself
compile proofs, scan the entire import graph, or prove external correctness.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TARGETS = [
    "CFSGComparator.classification",
    "CFSG.Milestones.cfsg_classification_native_and_realization",
]
ALLOWED = {"propext", "Quot.sound", "Classical.choice"}

def extract(log: str, target: str):
    # Lean convention: 'Some.Theorem' depends on axioms: [propext, Quot.sound]
    expr = re.compile(
        r"['\x60]?" + re.escape(target) +
        r"['\x60]?\s+depends on axioms:\s*\[([^\]]*)\]",
        flags=re.MULTILINE
    )
    matches = expr.findall(log)
    if len(matches) == 1:
        raw = matches[0]
        return [part.strip() for part in raw.split(",") if part.strip()], None
    empty = re.search(
        r"['\x60]?" + re.escape(target) +
        r"['\x60]?\s+does not depend on any axioms",
        log
    )
    if not matches and empty:
        return [], None
    return None, "Axiom output missing or ambiguous"

def evaluate(log: str) -> dict:
    results = []
    for name in TARGETS:
        axioms, error = extract(log, name)
        unexpected = sorted(set(axioms or []) - ALLOWED)
        valid = error is None and not unexpected
        results.append({
            "declaration": name,
            "status": "PASS" if valid else "FAIL",
            "observed_axioms": axioms,
            "unexpected_axioms": unexpected,
            "error": error
        })
    return {
        "schema_version": 1,
        "kind": "cfsg_final_axiom_output_check",
        "allowed_axioms": sorted(ALLOWED),
        "overall": "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL",
        "interpretation": "Pass checks actual printed Lean axiom names for these two declarations. It is not independent mathematical peer review.",
        "results": results
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--report", default="audit-results/axiom-results.json")
    args = parser.parse_args()
    log = Path(args.log).read_text(encoding="utf-8", errors="replace")
    result = evaluate(log)
    path = Path(args.report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["overall"] == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
