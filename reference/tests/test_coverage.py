"""Coverage and consistency checks for spec/signals.json, the vectors and the code.

Run from the repository root:

    PYTHONPATH=reference python3 -m unittest discover -s reference/tests
"""

import copy
import json
import pathlib
import re
import unittest

from open_signals.check import load_vectors, run_vector
from open_signals.rules import RULES, THRESHOLDS

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = json.loads((ROOT / "spec" / "signals.json").read_text(encoding="utf-8"))
VECTORS = load_vectors(ROOT / "spec" / "vectors")
SPEC_IDS = [rule["id"] for rule in SPEC["rules"]]


def github_anchor(heading):
    """The anchor GitHub generates for a Markdown heading."""
    text = heading.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(doc_path):
    lines = (ROOT / doc_path).read_text(encoding="utf-8").splitlines()
    return {github_anchor(line.lstrip("#")) for line in lines if line.startswith("#")}


def resolves(link):
    path, _, anchor = link.partition("#")
    if not (ROOT / path).is_file():
        return False
    return not anchor or anchor in anchors(path)


class SpecCoverage(unittest.TestCase):
    def test_rule_ids_unique(self):
        self.assertEqual(len(SPEC_IDS), len(set(SPEC_IDS)))

    def test_every_rule_has_an_implementation(self):
        self.assertEqual(sorted(SPEC_IDS), sorted(RULES), "spec rule IDs and RULES differ")

    def test_every_rule_has_a_vector(self):
        tested = {vector["rule"] for _, vector in VECTORS}
        self.assertEqual(sorted(set(SPEC_IDS) - tested), [], "rules with no vector")
        self.assertEqual(sorted(tested - set(SPEC_IDS)), [], "vectors for unknown rules")

    def test_case_coverage(self):
        cases = {}
        for _, vector in VECTORS:
            cases.setdefault(vector["rule"], set()).add(vector["case"])
        for rule in SPEC["rules"]:
            have = cases.get(rule["id"], set())
            need = {"pass", "fail"} | ({"boundary"} if rule.get("thresholds") else set())
            self.assertTrue(need <= have, "%s lacks cases %s" % (rule["id"], need - have))
            self.assertTrue(have <= set(SPEC["vector_cases"]), rule["id"])

    def test_vector_ids_unique(self):
        ids = [vector["id"] for _, vector in VECTORS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_ambiguous_rules_carry_notes(self):
        for rule in SPEC["rules"]:
            if rule.get("ambiguous"):
                self.assertTrue(rule.get("ambiguities"), rule["id"])


class DocLinks(unittest.TestCase):
    def test_spec_links_resolve(self):
        links = [t["doc"] for t in SPEC["thresholds"]] + [n["doc"] for n in SPEC["not_encoded"]]
        for rule in SPEC["rules"]:
            links.append(rule["doc"])
            links.extend(rule.get("also_cites", []))
            links.extend(a["doc"] for a in rule.get("ambiguities", []))
        for link in links:
            self.assertTrue(resolves(link), "unresolved doc link: %s" % link)

    def test_vector_links_resolve(self):
        for name, vector in VECTORS:
            self.assertTrue(resolves(vector["doc"]), "%s %s: %s" % (name, vector["id"], vector["doc"]))


class Thresholds(unittest.TestCase):
    def test_code_matches_spec(self):
        spec = {t["id"]: t["value"] for t in SPEC["thresholds"]}
        self.assertEqual(spec, THRESHOLDS)

    def test_thresholds_used_by_known_rules(self):
        for t in SPEC["thresholds"]:
            for rule in t["used_by"]:
                self.assertIn(rule, SPEC_IDS, t["id"])
        for rule in SPEC["rules"]:
            for tid in rule.get("thresholds", []):
                self.assertIn(tid, THRESHOLDS, rule["id"])

    def test_every_threshold_in_provenance_table(self):
        table = (ROOT / "docs" / "thresholds.md").read_text(encoding="utf-8")
        for t in SPEC["thresholds"]:
            self.assertIn("`%s`" % t["id"], table, t["id"])


class Runner(unittest.TestCase):
    def test_every_vector_passes(self):
        for name, vector in VECTORS:
            self.assertIsNone(run_vector(vector), "%s %s" % (name, vector["id"]))

    def test_runner_catches_a_wrong_expectation(self):
        _, vector = next((n, v) for n, v in VECTORS if v["id"] == "sr1a-doc-example-fires")
        broken = copy.deepcopy(vector)
        broken["expected"]["fires"] = False
        self.assertIsNotNone(run_vector(broken))
        broken = copy.deepcopy(vector)
        broken["expected"]["funding_dependence"] = 1.26
        self.assertIsNotNone(run_vector(broken))

    def test_runner_catches_a_missing_error(self):
        _, vector = next((n, v) for n, v in VECTORS if v["id"] == "ttm-too-few-quarters")
        broken = copy.deepcopy(vector)
        broken["inputs"]["fiscal_years"] = [{"ytd_3m": 1, "ytd_6m": 2, "ytd_9m": 3, "ytd_12m": 4}]
        self.assertIsNotNone(run_vector(broken))


if __name__ == "__main__":
    unittest.main()
