"""Safety and completeness tests for our read-only public-PR AI review."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("review", ROOT / "scripts" / "vgm_multi_ai_review.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class MultiAITests(unittest.TestCase):
    def test_safe_public_files(self):
        self.assertTrue(review.eligible_path("fontana-appliance-pickup/index.html"))
        self.assertTrue(review.eligible_path("scripts/example.js"))
        self.assertFalse(review.eligible_path("data/partners.json"))
        self.assertFalse(review.eligible_path(".env"))
        self.assertFalse(review.eligible_path("private_credentials.json"))
        self.assertFalse(review.eligible_path("assets/customer-photo.jpg"))

    def test_build_diff_skips_private_and_binary(self):
        diff, skipped, truncated = review.build_diff([
            {"filename": "index.html", "patch": "+Public page update"},
            {"filename": "data/lead-events.json", "patch": "+customer phone"},
            {"filename": "assets/photo.png"},
        ])
        self.assertIn("Public page update", diff)
        self.assertNotIn("customer phone", diff)
        self.assertEqual(len(skipped), 2)
        self.assertFalse(truncated)

    def test_build_diff_limits_large_patches(self):
        diff, skipped, truncated = review.build_diff([
            {"filename": "index.html", "patch": "A" * (review.MAX_PATCH_CHARS + 1)}
        ])
        self.assertEqual(diff, "")
        self.assertTrue(truncated)
        self.assertEqual(len(skipped), 1)

    def test_parse_valid_findings(self):
        raw = '{"findings": [{"severity": "high", "file": "index.html", "issue": "form gone", "evidence": "-<form>", "recommendation": "restore form"}]}'
        self.assertEqual(review.parse_review(raw)[0]["severity"], "high")

    def test_parse_fenced_json(self):
        self.assertEqual(review.parse_review('```json\n{"findings": []}\n```'), [])

    def test_invalid_model_output_not_a_pass(self):
        for bad in ('{"findings": "all good"}', '{"findings":[{"severity":"safe"}]}', 'looks fine'):
            with self.subTest(bad=bad):
                with self.assertRaises((ValueError, TypeError)):
                    review.parse_review(bad)

    def test_paid_or_unknown_models_rejected(self):
        for model in ("qwen/qwen3.8-27b", "openai/gpt-4o", "nvidia/nemotron-3-ultra:free"):
            with self.subTest(model=model):
                with self.assertRaises(ValueError):
                    review.call_free_model("fake", model, "test")

    def test_no_credentials_does_not_count_as_review(self):
        statuses = {label: {"model": model, "status": "not configured"} for label, model in review.REVIEWERS.items()}
        _, state = review.report_markdown(1, statuses, [], False, True)
        self.assertIn("INCOMPLETE", state)

    def test_one_model_insufficient(self):
        labels = list(review.REVIEWERS)
        statuses = {labels[0]: {"model": review.REVIEWERS[labels[0]], "status": "reviewed", "findings": []}}
        _, state = review.report_markdown(1, statuses, [], False, True)
        self.assertIn("INCOMPLETE", state)

    def test_dual_review_has_no_approval(self):
        statuses = {label: {"model": model, "status": "reviewed", "findings": []} for label, model in review.REVIEWERS.items()}
        markdown, state = review.report_markdown(1, statuses, [], False, True)
        self.assertIn("ADVISORY COMPLETE", state)
        self.assertIn("NOT an approval", markdown)

    def test_high_risk_must_be_reviewed(self):
        statuses = {label: {"model": model, "status": "reviewed", "findings": []} for label, model in review.REVIEWERS.items()}
        first = next(iter(statuses.values()))
        first["findings"] = [{"severity": "critical", "file": "index.html", "issue": "form removed",
                             "evidence": "-form", "recommendation": "restore form"}]
        _, state = review.report_markdown(1, statuses, [], False, True)
        self.assertIn("NEEDS HUMAN REVIEW", state)

    def test_skipped_files_cannot_be_marked_complete(self):
        """Reviewing only part of a PR must never look like complete coverage."""
        statuses = {label: {"model": model, "status": "reviewed", "findings": []}
                    for label, model in review.REVIEWERS.items()}
        markdown, state = review.report_markdown(
            1, statuses, ["data/lead-events.json"], False, True
        )
        self.assertIn("INCOMPLETE", state)
        self.assertIn("omitted", state)
        self.assertIn("data/lead-events.json", markdown)

    def test_incomplete_independent_review_fails_gitHub_check(self):
        # Incomplete/at-risk reports must not make the independent-AI job green.
        self.assertEqual(review.review_exit_code(
            "INCOMPLETE — two independent AI reviews not available"), 1)
        self.assertEqual(review.review_exit_code(
            "INCOMPLETE — some changed files were omitted from AI review"), 1)
        self.assertEqual(review.review_exit_code(
            "NEEDS HUMAN REVIEW — high/critical findings"), 1)
        self.assertEqual(review.review_exit_code(
            "ADVISORY COMPLETE — still requires tests and human/CI review"), 0)

    def test_truncated_review_is_incomplete(self):
        statuses = {label: {"model": model, "status": "reviewed", "findings": []} for label, model in review.REVIEWERS.items()}
        _, state = review.report_markdown(1, statuses, ["too many"], True, True)
        self.assertIn("INCOMPLETE", state)


if __name__ == "__main__":
    unittest.main()
