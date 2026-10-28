#!/usr/bin/env python3
"""Synthetic unit tests for the final-axiom log parser (not CFSG proof tests)."""
import unittest
from verify_cfsg_axioms import evaluate

A = "CFSGComparator.classification"
B = "CFSG.Milestones.cfsg_classification_native_and_realization"

class ParseAxiomOutputTests(unittest.TestCase):
    def test_standard_axioms_pass(self):
        log = (
            "'" + A + "' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
            "'" + B + "' depends on axioms: [Quot.sound, Classical.choice, propext]\n"
        )
        outcome = evaluate(log)
        self.assertEqual(outcome["overall"], "PASS")

    def test_unexpected_sorry_axiom_fails(self):
        log = (
            "'" + A + "' depends on axioms: [propext, sorryAx]\n"
            "'" + B + "' depends on axioms: [Quot.sound]\n"
        )
        outcome = evaluate(log)
        self.assertEqual(outcome["overall"], "FAIL")
        self.assertIn("sorryAx", outcome["results"][0]["unexpected_axioms"])

    def test_missing_target_fails(self):
        log = "'" + A + "' depends on axioms: [propext]\n"
        self.assertEqual(evaluate(log)["overall"], "FAIL")

    def test_duplicate_output_fails(self):
        log = (
            "'" + A + "' depends on axioms: [propext]\n"
            "'" + A + "' depends on axioms: [Quot.sound]\n"
            "'" + B + "' depends on axioms: [Classical.choice]\n"
        )
        self.assertEqual(evaluate(log)["overall"], "FAIL")

    def test_axiom_free_declaration_passes(self):
        log = (
            "'" + A + "' does not depend on any axioms\n"
            "'" + B + "' depends on axioms: [propext]\n"
        )
        self.assertEqual(evaluate(log)["overall"], "PASS")

if __name__ == "__main__":
    unittest.main()
