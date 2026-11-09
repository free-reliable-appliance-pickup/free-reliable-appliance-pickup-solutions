"""Read-only FastTrack release-readiness gate regressions."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts.ttg_release_readiness import assess, dated, evidence_check, staged_cities


class OperationalGate(unittest.TestCase):
    """The technical stage can pass while operational launch stays blocked."""

    def test_real_il_staging_stays_request_only(self):
        """Current 61 live-stage pages do not imply an accepting local operator."""
        result = assess("IL")
        self.assertEqual(result["pages"], 61)
        self.assertEqual(len(result["cities"]), 12)
        self.assertTrue(result["request_only_safe"], result["technical_errors"])
        self.assertFalse(result["operational_prerequisites_recorded"])
        self.assertFalse(result["index_activation_authorized"])
        self.assertTrue(any("Formspree" in x for x in result["operational_blockers"]))
        self.assertTrue(any("operator" in x for x in result["operational_blockers"]))

    def test_recognize_only_owner_city_pages(self):
        """Category and statewide hub pages are not separately operated cities."""
        pages = [
            "illinois-appliance-pickup/index.html",
            "chicago-il-appliance-pickup/index.html",
            "chicago-il-stove-oven-pickup/index.html",
            "aurora-il-appliance-pickup/index.html",
        ]
        self.assertEqual(staged_cities(pages, "IL"), ["aurora", "chicago"])

    def test_no_operator_or_receipt_blocks_launch(self):
        """Missing operator, receipt and signoff remain visible blockers."""
        verified, issues = evidence_check(
            {"verified_cities": [], "form_receipt": {"verified": False},
             "owner_release_approval": {"approved": False}},
            ["chicago"], "chicago")
        self.assertEqual(verified, [])
        self.assertGreaterEqual(len(issues), 3)

    def test_complete_evidence_does_not_auto_index(self):
        """Synthetic proof tests syntax only and cannot authorize publication."""
        evidence = {
            "form_receipt": {"verified": True, "verified_on": "2026-11-09",
                             "receipt_reference": "owner-inbox-check"},
            "owner_release_approval": {"approved": True, "approved_on": "2026-11-09",
                                       "reference": "manual-approval"},
            "verified_cities": [
                {"city_slug": "chicago", "zip_codes": ["60601"],
                 "operator_reference": "restricted-operations-record",
                 "pickup_terms_checked": True, "verified_on": "2026-11-09"},
            ],
        }
        verified, errors = evidence_check(evidence, ["chicago"], "chicago")
        self.assertEqual(verified, ["chicago"])
        self.assertEqual(errors, [])
        # This tests validation logic using synthetic evidence, not real Chicago coverage.
        self.assertFalse(assess("IL")["index_activation_authorized"])

    def test_invalid_zip_and_invalid_calendar_date_rejected(self):
        """Reject incomplete ZIP coverage and invalid calendar dates."""
        self.assertFalse(dated("2026-13-77"))
        verified, issues = evidence_check({
            "verified_cities": [{
                "city_slug": "chicago", "zip_codes": ["000"],
                "operator_reference": "review", "pickup_terms_checked": True,
                "verified_on": "2026-11-09",
            }]
        }, ["chicago"])
        self.assertEqual(verified, [])
        self.assertTrue(any("Incomplete" in x for x in issues))

    def test_unknown_city_does_not_pass_technical_preflight(self):
        """A city absent from the manifest cannot get release clearance."""
        result = assess("IL", city="invented-illinois-city")
        self.assertFalse(result["request_only_safe"])
        self.assertTrue(any("not in the stage manifest" in e
                            for e in result["technical_errors"]))

    def test_nonobject_evidence_is_rejected(self):
        """A JSON list cannot supply release evidence."""
        verified, errors = evidence_check([], ["chicago"])
        self.assertEqual(verified, [])
        self.assertTrue(any("invalid readiness ledger" in e for e in errors))

    def test_missing_manifest_is_blocked(self):
        """Require a real page manifest instead of passing an empty batch."""
        with tempfile.TemporaryDirectory() as t:
            result = assess("IL", root=Path(t))
        self.assertFalse(result["request_only_safe"])
        self.assertFalse(result["index_activation_authorized"])
        self.assertTrue(result["technical_errors"])


if __name__ == "__main__":
    unittest.main()
