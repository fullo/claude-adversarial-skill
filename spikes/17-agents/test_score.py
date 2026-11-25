"""Tests of score.py: each rule of the scoring on a report built to exercise it.

Run: python3 -m unittest discover -s spikes/17-agents -p 'test_score.py'
"""

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score as S  # noqa: E402

KEY = {"case": "X", "defects": [
    {"id": "A", "file": "scripts/a.py", "first_line": 10, "last_line": 10, "keywords": ["sep"]},
    {"id": "B", "file": "scripts/a.py", "first_line": 40, "last_line": 41, "keywords": ["badges[:1]"]},
    {"id": "C", "file": "README.md", "first_line": 3, "last_line": 3, "keywords": ["currently 4.1"]},
    {"id": "D", "file": "scripts/b.py", "first_line": 5, "last_line": 5, "keywords": ["toolchain"]},
    {"id": "E", "file": "scripts/a.py", "first_line": 44, "last_line": 44, "keywords": ["never-said"]},
]}

FAIL = "| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |\n|---|---|---|---|---|---|---|---|---|\n"
HIDDEN = "| # | Location | Advertised | Actual | Type (if a problem) | Confidence |\n|---|---|---|---|---|---|\n"
HYP = "| # | Observation | Hypothesis | Alternative | Test to confirm |\n|---|---|---|---|---|\n"


class ScoreTest(unittest.TestCase):
    def setUp(self):
        self.tree = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tree, "scripts"))
        a = ["x = 1"] * 60
        a[9] = 'SEP = r"[\\W_]?"  # separator'
        a[39] = "for b in badges[:1]:"
        open(os.path.join(self.tree, "scripts/a.py"), "w").write("\n".join(a) + "\n")
        open(os.path.join(self.tree, "scripts/b.py"), "w").write("one\nif a | b:\nthree\nfour\nskip toolchain\n")
        open(os.path.join(self.tree, "README.md"), "w").write("# T\n\nThe plugin is (currently 4.1).\n")

    def tearDown(self):
        shutil.rmtree(self.tree, ignore_errors=True)

    def run_score(self, report):
        return S.score(report, KEY, self.tree)

    def test_a_fail_row_near_the_line_finds_the_defect(self):
        r = self.run_score(FAIL + '| 1 | scripts/a.py:12 | `SEP = r"[\\W_]?"` | Demonstrated defect | high | s | Deductive | 85 | f |\n')
        self.assertEqual((r["status"]["A"], r["matched_by"]["A"]), ("found", "line"))
        self.assertEqual(r["found"], 1)
        self.assertEqual(r["recall"], 0.2)

    def test_a_line_outside_the_window_matches_only_with_a_keyword(self):
        far = FAIL + "| 1 | scripts/a.py:30 | `x = 1` | Demonstrated defect | high | {} | Deductive | 85 | f |\n"
        self.assertEqual(self.run_score(far.format("something else"))["status"]["A"], "missed")
        r = self.run_score(far.format("the SEP pattern allows one character"))
        self.assertEqual((r["status"]["A"], r["matched_by"]["A"]), ("found", "keyword"))

    def test_the_window_is_inclusive_at_five_lines_and_not_at_six(self):
        row = FAIL + "| 1 | scripts/a.py:{} | `x = 1` | Demonstrated defect | high | s | Deductive | 85 | f |\n"
        self.assertEqual(self.run_score(row.format(15))["status"]["A"], "found")
        self.assertEqual(self.run_score(row.format(16))["status"]["A"], "missed")
        self.assertEqual(self.run_score(row.format(5))["status"]["A"], "found")
        self.assertEqual(self.run_score(row.format(4))["status"]["A"], "missed")

    def test_the_same_keyword_in_another_file_is_not_a_match(self):
        r = self.run_score(FAIL + "| 1 | scripts/b.py:30 | `one` | Demonstrated defect | high | the SEP pattern | Deductive | 85 | f |\n")
        self.assertEqual(r["status"]["A"], "missed")
        self.assertEqual(len(r["unmatched_fail_rows"]), 1)

    def test_a_file_cited_by_its_name_alone_matches(self):
        r = self.run_score(FAIL + "| 1 | a.py:40 | `for b in badges[:1]:` | Demonstrated defect | high | s | Deductive | 85 | f |\n")
        self.assertEqual(r["status"]["B"], "found")

    def test_hidden_and_hypothesis_are_reported_but_not_found(self):
        report = (HIDDEN + "| 1 | scripts/b.py:5 | fails | skips | Demonstrated defect | 80 |\n\n"
                  + HYP + "| 1 | README.md says (currently 4.1) | stale | none | compare |\n")
        r = self.run_score(report)
        self.assertEqual((r["status"]["D"], r["status"]["C"]), ("hidden", "hypothesis"))
        self.assertEqual((r["found"], r["hidden"], r["hypothesis_only"], r["missed"]), (0, 1, 1, 3))

    def test_one_row_finds_by_its_line_only_the_nearest_of_two_close_defects(self):
        row = FAIL + "| 1 | scripts/a.py:{} | `x = 1` | Demonstrated defect | high | {} | Deductive | 85 | f |\n"
        r = self.run_score(row.format(41, "s"))  # B is at 40-41, E at 44: both inside the window
        self.assertEqual((r["status"]["B"], r["status"]["E"]), ("found", "missed"))
        r = self.run_score(row.format(43, "s"))
        self.assertEqual((r["status"]["B"], r["status"]["E"]), ("missed", "found"))
        r = self.run_score(row.format(43, "and badges[:1] two lines above"))  # the other one named by a keyword
        self.assertEqual((r["status"]["B"], r["status"]["E"]), ("found", "found"))

    def test_a_fail_row_wins_over_a_hidden_row_for_the_same_defect(self):
        report = (HIDDEN + "| 1 | scripts/b.py:5 | fails | skips | - | 80 |\n\n"
                  + FAIL + "| 1 | scripts/b.py:5 | `skip toolchain` | Demonstrated defect | high | s | Deductive | 85 | f |\n")
        self.assertEqual(self.run_score(report)["status"]["D"], "found")

    def test_citations_verified_wrong_line_and_unverifiable(self):
        report = FAIL + (
            "| 1 | scripts/a.py:40 | `for b in badges[:1]:` | Demonstrated defect | high | s | Deductive | 85 | f |\n"
            "| 2 | scripts/a.py:10 | `for b in badges[:1]:` | Demonstrated defect | high | s | Deductive | 85 | f |\n"
            "| 3 | scripts/a.py:10 | `for b in every_badge:` | Demonstrated defect | high | s | Deductive | 85 | f |\n"
            "| 4 | scripts/nosuch.py:3 | `x = 1` | Demonstrated defect | high | s | Deductive | 85 | f |\n"
            "| 5 | scripts/a.py | `x = 1` | Preventive measure | low | s | Inductive | 60 | f |\n")
        r = self.run_score(report)
        self.assertEqual((r["citations_checked"], r["citations_verified"], r["citations_wrong_line"], r["citations_unverifiable"]),
                         (4, 1, 1, 2))

    def test_a_cut_quote_is_checked_piece_by_piece(self):
        row = FAIL + "| 1 | scripts/a.py:10 | `SEP = r... # {}` | Demonstrated defect | high | s | Deductive | 85 | f |\n"
        self.assertEqual(self.run_score(row.format("separator"))["citations_verified"], 1)
        self.assertEqual(self.run_score(row.format("something invented"))["citations_unverifiable"], 1)

    def test_an_escaped_pipe_and_a_pipe_in_code_stay_in_their_cell(self):
        r = self.run_score(FAIL + "| 1 | scripts/b.py:2 | `if a | b:` | Demonstrated defect | high | a \\| b | Deductive | 85 | f |\n")
        self.assertEqual(r["citations_verified"], 1)
        self.assertEqual(r["fail_rows"], 1)

    def test_a_report_with_no_table_scores_zero_and_does_not_fail(self):
        r = self.run_score("Nothing to report.\n")
        self.assertEqual((r["found"], r["rows"], r["recall"]), (0, 0, 0.0))

    def test_unmatched_fail_rows_are_listed_not_judged(self):
        r = self.run_score(FAIL + "| 1 | scripts/b.py:30 | `one` | Preventive measure | low | naming | Inductive | 60 | rename |\n")
        self.assertEqual([u["file"] for u in r["unmatched_fail_rows"]], ["scripts/b.py"])
        self.assertNotIn("false_positives", r)


if __name__ == "__main__":
    unittest.main()
