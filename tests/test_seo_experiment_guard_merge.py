#!/usr/bin/env python3
"""Guard regression tests in isolated git repos; never touch live site files."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "scripts" / "seo-experiment-guard.py"


def git(folder, *args):
    return subprocess.run(
        ["git", *args], cwd=folder, text=True, capture_output=True, check=True
    ).stdout.strip()


class GuardMergeContextTests(unittest.TestCase):
    def run_case(self, commit_message, is_merge, expect_success, earlier_nontechnical=False, as_pr=False):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            git(folder, "init", "-q", "-b", "main")
            git(folder, "config", "user.email", "test@example.invalid")
            git(folder, "config", "user.name", "SEO Guard Test")
            (root / "data").mkdir()
            (root / "city").mkdir()
            today = date.today()
            experiment = {
                "experiments": [{
                    "id": "guard-fixture",
                    "status": "running",
                    "lastChanged": today.isoformat(),
                    "evaluateNotBefore": (today + timedelta(days=14)).isoformat(),
                    "pagesChanged": ["/city/"],
                }]
            }
            (root / "data" / "seo-experiments.json").write_text(json.dumps(experiment))
            (root / "city" / "index.html").write_text("<h1>Original</h1>")
            git(folder, "add", ".")
            git(folder, "commit", "-qm", "Initial experiment and protected city")
            if as_pr:
                git(folder, "remote", "add", "origin", folder)
                git(folder, "fetch", "-q", "origin", "main:refs/remotes/origin/main")
            if is_merge or as_pr:
                git(folder, "checkout", "-qb", "feature")
            if earlier_nontechnical:
                (root / "city" / "index.html").write_text("<h1>Unapproved speculative change</h1>")
                git(folder, "add", ".")
                git(folder, "commit", "-qm", "Speculative copy rewrite")
            (root / "city" / "index.html").write_text("<h1>Changed</h1>")
            git(folder, "add", ".")
            git(folder, "commit", "-qm", commit_message)
            if is_merge:
                git(folder, "checkout", "-q", "main")
                git(folder, "merge", "--no-ff", "-qm", "Merge pull request #1535", "feature")
            env = dict(os.environ)
            env.pop("GITHUB_BASE_REF", None)
            if as_pr:
                env["GITHUB_BASE_REF"] = "main"
            result = subprocess.run(
                [sys.executable, str(GUARD)],
                cwd=folder, env=env, capture_output=True, text=True,
            )
            self.assertEqual(
                result.returncode == 0, expect_success,
                f"stdout: {result.stdout}\nstderr: {result.stderr}",
            )
            if expect_success:
                self.assertIn("technical override", result.stdout)
            else:
                self.assertIn("SEO_EXPERIMENT_GUARD_BLOCK", result.stdout)

    def test_merged_technical_change_allowed(self):
        self.run_case("[technical-fix] Validated ZIP correction", True, True)

    def test_merged_nontechnical_change_blocked(self):
        self.run_case("Speculative city copy rewrite", True, False)

    def test_merged_mixed_commit_branch_blocked(self):
        # Final commit is technical but an earlier protected-page edit is not.
        self.run_case("[technical-fix] A later valid correction", True, False, earlier_nontechnical=True)

    def test_pr_technical_change_allowed(self):
        self.run_case("[technical-fix] Validated ZIP correction", False, True, as_pr=True)

    def test_pr_mixed_commit_branch_blocked(self):
        self.run_case("[technical-fix] A later valid correction", False, False,
                      earlier_nontechnical=True, as_pr=True)

    def test_direct_technical_change_allowed(self):
        self.run_case("[technical-fix] Correct contact details", False, True)

    def test_direct_nontechnical_change_blocked(self):
        self.run_case("Speculative city copy rewrite", False, False)


if __name__ == "__main__":
    unittest.main()
