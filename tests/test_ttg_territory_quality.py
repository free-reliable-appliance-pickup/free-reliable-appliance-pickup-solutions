"""Strict unit tests with synthetic identities only: never use real customer data."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ttg_territory_quality_report import build_report


def item(lead, item_id="a", **overrides):
    row = {
        "lead_id": str(lead), "item_id": str(item_id),
        "received_at": "2026-10-14T11:00:00", "state_code": "MD",
        "territory_id": "MD-WASHINGTON-SUBURBS",
        "appliance_type": "refrigerator", "working_status": "verified_working",
        "quality_grade": "A", "photos_received": "yes",
        "partner_status": "accepted", "pickup_status": "completed",
        "resale_price_cents": "30000", "acquisition_cost_cents": "1000",
        "transport_cost_cents": "3000", "repair_cost_cents": "2000",
        "lead_fee_cents": "500", "zip": "20910", "partner_id": "synthetic-partner",
    }
    row.update(overrides)
    return row


def partner(id, **overrides):
    p = {
        "partner_id": str(id), "state_code": "MD",
        "territory_id": "MD-WASHINGTON-SUBURBS", "month": "2026-10",
        "active": "true", "renewal_observed": "true",
        "renewed_next_month": "true",
    }
    p.update(overrides)
    return p


class TerritoryQualityTests(unittest.TestCase):
    def test_unique_leads_are_not_items_and_net_is_realized(self):
        rows = [item(i) for i in range(1, 6)]
        rows.append(item(1, "b", working_status="reported_working", quality_grade="unknown",
                         resale_price_cents="", transport_cost_cents=""))
        x = build_report(rows)["territories"][0]
        self.assertEqual(x["unique_leads"], 5)
        self.assertEqual(x["appliance_items"], 6)
        self.assertEqual(x["reported_or_verified_working_items"], 6)
        self.assertEqual(x["verified_working_items"], 5)
        self.assertEqual(x["verified_grade_a_b_items"], 5)
        self.assertEqual(x["partner_accepted_leads"], 5)
        self.assertEqual(x["completed_pickup_leads"], 5)
        self.assertEqual(x["items_missing_realized_margin"], 1)
        self.assertEqual(x["items_with_realized_net_margin"], 5)
        self.assertEqual(x["average_realized_net_margin_cents"], 23500)
        self.assertEqual(x["total_realized_net_margin_cents"], 117500)

    def test_small_cohort_is_suppressed_and_no_leads_made_up(self):
        x = build_report([item(i) for i in range(1, 5)])
        self.assertEqual(x["territories"], [])
        self.assertEqual(x["metadata"]["suppressed_small_cohorts"], 1)
        self.assertEqual(build_report([])["metadata"]["has_observed_rows"], False)

    def test_early_customer_quality_claim_cannot_be_a(self):
        with self.assertRaisesRegex(ValueError, "A/B grade requires"):
            build_report([item(1, working_status="reported_working")])

    def test_duplicate_item_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            build_report([item(1), copy.copy(item(1))])

    def test_realized_profit_is_unknown_when_cost_missing(self):
        rows = [item(i, lead_fee_cents="") for i in range(1, 6)]
        x = build_report(rows)["territories"][0]
        self.assertIsNone(x["average_realized_net_margin_cents"])
        self.assertEqual(x["items_with_realized_net_margin"], 0)
        self.assertEqual(x["items_missing_realized_margin"], 5)

    def test_partner_renewal_requires_observed_sample(self):
        rows = [item(i) for i in range(1, 6)]
        small = build_report(rows, [partner(1), partner(2)])["territories"][0]
        self.assertIsNone(small["observed_next_month_renewal_rate_pct"])
        large = build_report(rows, [partner(1), partner(2, renewed_next_month="false"),
                                    partner(3)])["territories"][0]
        self.assertEqual(large["observed_next_month_renewal_rate_pct"], 66.7)
        self.assertEqual(large["renewal_outcomes_observed"], 3)

    def test_no_customer_or_partner_ids_in_json(self):
        rows = [item(i, zip="20910", partner_id="PRIVATE-OPERATOR") for i in range(1, 6)]
        as_text = json.dumps(build_report(rows))
        for private in ("lead_id", "partner_id", "20910", "PRIVATE-OPERATOR"):
            self.assertNotIn(private, as_text)

    def test_no_tiny_privacy_thresholds(self):
        with self.assertRaisesRegex(ValueError, "Privacy minimums"):
            build_report([item(1)], min_leads=1)

    def test_unobserved_renewal_must_not_be_true(self):
        with self.assertRaisesRegex(ValueError, "unobserved"):
            build_report([item(i) for i in range(1, 6)],
                         [partner(1, renewal_observed="false")])

    def test_same_id_in_two_market_months_rejected(self):
        with self.assertRaisesRegex(ValueError, "reused"):
            build_report([item(1), item(1, "b", state_code="VA")])


if __name__ == "__main__":
    unittest.main()
