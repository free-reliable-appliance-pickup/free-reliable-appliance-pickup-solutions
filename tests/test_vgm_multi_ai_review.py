"""Safety and completeness tests for our read-only public-PR AI review."""
import importlib.util
import json
from io import BytesIO
from unittest.mock import patch
import pathlib
import unittest
import subprocess
import sys

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

    def test_leading_think_block_can_precede_verified_json(self):
        content = '<think>Draft thoughts, not a review.</think>\n```json\n{"findings":[] }\n```'
        self.assertEqual(review.parse_review(content), [])

    def test_invalid_review_response_has_safe_fixed_category(self):
        for payload, category in (
            (None, "empty_or_nontext_response"),
            ("", "empty_or_nontext_response"),
            ("not json", "invalid_json"),
            ('{"findings":"ok"}', "invalid_findings_schema"),
            ('{"findings":[{"severity":"safe"}]}', "invalid_finding"),
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(review.ModelOutputError) as ctx:
                    review.parse_review(payload)
                self.assertEqual(ctx.exception.category, category)

    def test_report_discloses_http_code_not_secret_or_upstream_body(self):
        statuses = {
            "Independent code reviewer (Nemotron 3.5 Super VL)": {
                "model": review.REVIEWERS["Independent code reviewer (Nemotron 3.5 Super VL)"],
                "status": "unavailable",
                "error": "ModelOutputError",
                "output_issue": "invalid_json",
            },
            "Independent site/SEO reviewer (Dots Studio)": {
                "model": review.REVIEWERS["Independent site/SEO reviewer (Dots Studio)"],
                "status": "unavailable",
                "error": "HTTPError",
                "http_status": 429,
            },
        }
        markdown, state = review.report_markdown(911, statuses, [], False, True)
        self.assertIn("INCOMPLETE", state)
        self.assertIn("HTTP status: 429", markdown)
        self.assertIn("Output issue: invalid_json", markdown)
        self.assertNotIn("sk-or-v1", markdown)
        self.assertEqual(review.review_exit_code(state), 1)

    def test_empty_final_answer_reports_only_safe_finish_reason(self):
        responses = (("length", "empty_or_nontext_response_finish_length"),
                     ("stop", "empty_or_nontext_response_finish_stop"),
                     ("surprising_private_value", "empty_or_nontext_response_finish_other"))
        for finish, expected in responses:
            with self.subTest(finish=finish):
                payload = {"choices": [{"finish_reason": finish,
                                        "message": {"content": None,
                                                    "reasoning": "never log this text"}}]}
                with patch.object(review, "urlopen",
                                  return_value=BytesIO(json.dumps(payload).encode())):
                    with self.assertRaises(review.ModelOutputError) as context:
                        review.call_free_model("fake", next(iter(review.REVIEWERS.values())), "diff")
                self.assertEqual(context.exception.category, expected)
                self.assertNotIn("never log", str(context.exception))

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

    def test_two_distinct_verified_free_reviewers(self):
        self.assertEqual(review.REVIEWERS, {
            "Independent code reviewer (Nemotron 3.5 Super VL)": "nvidia/nemotron-3.5-super-vl:free",
            "Independent site/SEO reviewer (Dots Studio)": "dots-studio/dots-3-note-preview:free",
        })
        self.assertEqual(len(set(review.REVIEWERS.values())), 2)
        self.assertTrue(all(m.endswith(":free") for m in review.REVIEWERS.values()))

    def test_free_reviewers_request_strict_json_without_network(self):
        expected = {"choices": [{"message": {"content": '{"findings":[]}'}}]}
        for model in review.REVIEWERS.values():
            with self.subTest(model=model):
                with patch.object(review, "urlopen", return_value=BytesIO(json.dumps(expected).encode())) as mock:
                    self.assertEqual(review.call_free_model("test-only", model, "patch"), [])
                    request = mock.call_args[0][0]
                    body = json.loads(request.data)
                    self.assertEqual(body["model"], model)
                    self.assertEqual(body["response_format"], {"type": "json_object"})
                    self.assertEqual(body["messages"][1]["content"], "patch")
                    self.assertEqual(body["max_tokens"], 5000)
                    self.assertEqual(body["reasoning"], {"enabled": False})

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


class QuotaGateWorkflowTests(unittest.TestCase):
    """Synthetic event tests for the required, fail-closed review job."""

    def test_release_label_gate(self):
        text = (ROOT / ".github/workflows/vgm-independent-multi-ai.yml").read_text()
        self.assertIn("types: [opened, synchronize, reopened, labeled, unlabeled, edited]", text)
        self.assertIn("Refuse non-selected or external release PRs", text)
        self.assertIn("sys.exit(1)", text)
        self.assertLess(text.index("Refuse non-selected"), text.index("Checkout TRUSTED"))
        self.assertLess(text.index("Refuse non-selected"),
                        text.index("Independent reviews — two approved FREE models only"))
        self.assertIn("    if: ${{ !cancelled() }}", text)  # Required job runs unless explicitly canceled.
        self.assertNotIn("    if: >-", text)  # Skipped required jobs can pass.
        self.assertIn("'unrelated-label' || 'release'", text)  # Other labels cannot cancel selected review.
        self.assertIn("workflow_dispatch:", text)
        marker = "          python3 - <<'PY'\n"
        self.assertEqual(text.count(marker), 1)
        snippet = text.split(marker, 1)[1].split("\n          PY", 1)[0]
        script = "\n".join(line[10:] if line.startswith("          ") else line
                           for line in snippet.splitlines())
        cases = (
            ("selected synchronize", ["vgm-release-review"], "synchronize", "", "owner/repo", 0),
            ("selected label", ["vgm-release-review"], "labeled", "vgm-release-review", "owner/repo", 0),
            ("no label", [], "opened", "", "owner/repo", 1),
            ("no label after edit", [], "edited", "", "owner/repo", 1),
            ("removed label", [], "unlabeled", "vgm-release-review", "owner/repo", 1),
            ("unrelated label", ["vgm-release-review"], "labeled", "other", "owner/repo", 1),
            ("fork", ["vgm-release-review"], "synchronize", "", "fork/repo", 1),
        )
        for name, labels, action, event_label, head_repo, expected in cases:
            with self.subTest(name=name):
                env = {"REVIEW_LABELS": json.dumps(labels), "PR_HEAD_REPO": head_repo,
                       "TRUSTED_REPO": "owner/repo", "EVENT_ACTION": action,
                       "EVENT_LABEL": event_label}
                proc = subprocess.run([sys.executable, "-c", script], env=env,
                                      capture_output=True, text=True, timeout=5)
                self.assertEqual(proc.returncode, expected,
                                 msg=f"{name}: {proc.stdout} {proc.stderr}")


if __name__ == "__main__":
    unittest.main()
