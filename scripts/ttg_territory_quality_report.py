#!/usr/bin/env python3
"""Private TTG territory-quality report. Inputs stay local; output is aggregate-only.

Usage:
  python scripts/ttg_territory_quality_report.py --input private-items.csv \
    --partner-months private-partners.csv --output private-report.json

Never commit real input/output containing confidential operational facts to public Git.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

REQUIRED = (
    "lead_id", "item_id", "received_at", "state_code", "territory_id",
    "appliance_type", "working_status", "quality_grade", "photos_received",
    "partner_status", "pickup_status",
)
PARTNER_REQUIRED = (
    "partner_id", "state_code", "territory_id", "month", "active",
    "renewal_observed", "renewed_next_month",
)
ALLOWED = {
    "working_status": {"reported_working", "verified_working", "needs_repair", "not_working", "unknown"},
    "quality_grade": {"A", "B", "C", "D", "unknown"},
    "partner_status": {"accepted", "declined", "unoffered"},
    "pickup_status": {"completed", "cancelled", "pending", "no_coverage"},
    "appliance_type": {"washer", "dryer", "washer_dryer_set", "refrigerator", "freezer", "stove", "range", "oven", "other"},
}


def read_csv(path: str | Path, required: tuple[str, ...]) -> list[dict[str, str]]:
    """Read a PRIVATE local CSV; never persist, transmit, or echo its raw rows."""
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = set(required) - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
        return list(reader)


def yes(value: str) -> bool:
    v = (value or "").strip().lower()
    if v not in {"true", "false", "yes", "no", "1", "0"}:
        raise ValueError("Boolean value must be true/false, yes/no, or 1/0")
    return v in {"true", "yes", "1"}


def cents(value: str | None) -> int | None:
    if value is None or not str(value).strip():
        return None
    try:
        amount = int(str(value).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError("Money must be a non-negative integer number of cents") from exc
    if amount < 0:
        raise ValueError("Money must be a non-negative integer number of cents")
    return amount


def pct(numerator: int, denominator: int) -> float | None:
    return round(100.0 * numerator / denominator, 1) if denominator else None


def build_report(
    items: list[dict[str, str]],
    partner_months: list[dict[str, str]] | None = None,
    min_leads: int = 5,
    min_partners: int = 3,
) -> dict:
    if min_leads < 5 or min_partners < 3:
        raise ValueError("Privacy minimums cannot be below 5 leads or 3 partner accounts")

    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    known_items: set[tuple[str, str]] = set()
    lead_locations: dict[str, tuple[str, str, str]] = {}
    for raw in items:
        for column in REQUIRED:
            if not str(raw.get(column, "") or "").strip():
                raise ValueError("Missing required value: " + column)
        for column, allowed in ALLOWED.items():
            if raw[column] not in allowed:
                raise ValueError("Unexpected value for " + column)
        if raw["quality_grade"] in {"A", "B"} and raw["working_status"] != "verified_working":
            raise ValueError("A/B grade requires independently verified working status")
        photos = yes(raw["photos_received"])
        try:
            month = date.fromisoformat(raw["received_at"][:10]).isoformat()[:7]
        except ValueError as exc:
            raise ValueError("received_at must start with a real ISO date") from exc
        state = raw["state_code"].upper()
        if len(state) != 2 or not state.isalpha():
            raise ValueError("state_code must contain two letters")
        key = (state, raw["territory_id"], month)
        item_key = (raw["lead_id"], raw["item_id"])
        if item_key in known_items:
            raise ValueError("Duplicate item_id within the same lead")
        known_items.add(item_key)
        if raw["lead_id"] in lead_locations and lead_locations[raw["lead_id"]] != key:
            raise ValueError("A lead_id cannot be reused across territories or months")
        lead_locations[raw["lead_id"]] = key
        money = [cents(raw.get(f)) for f in (
            "resale_price_cents", "acquisition_cost_cents",
            "transport_cost_cents", "repair_cost_cents", "lead_fee_cents",
        )]
        groups[key].append({
            "lead": raw["lead_id"],
            "working": raw["working_status"],
            "grade": raw["quality_grade"],
            "photos": photos,
            "partner": raw["partner_status"],
            "pickup": raw["pickup_status"],
            "money": money,
        })

    renewal: dict[tuple[str, str, str], list[bool]] = defaultdict(list)
    seen_partner_months: set[tuple[str, str, str, str]] = set()
    for raw in partner_months or []:
        for column in PARTNER_REQUIRED:
            if not str(raw.get(column, "") or "").strip():
                raise ValueError("Missing required partner-month value: " + column)
        try:
            date.fromisoformat(raw["month"] + "-01")
        except ValueError as exc:
            raise ValueError("Partner month must be YYYY-MM") from exc
        state = raw["state_code"].upper()
        group = (state, raw["territory_id"], raw["month"])
        identity = (*group, raw["partner_id"])
        if identity in seen_partner_months:
            raise ValueError("Duplicate partner-month in territory")
        seen_partner_months.add(identity)
        active, observed, renewed = (
            yes(raw["active"]), yes(raw["renewal_observed"]),
            yes(raw["renewed_next_month"]),
        )
        if renewed and not active:
            raise ValueError("Cannot renew an inactive partner")
        if renewed and not observed:
            raise ValueError("Renewal cannot be true when unobserved")
        if active and observed:
            renewal[group].append(renewed)

    report = []
    suppressed = 0
    for key, rows in sorted(groups.items()):
        leads = {x["lead"] for x in rows}
        if len(leads) < min_leads:
            suppressed += 1
            continue
        verified = sum(x["working"] == "verified_working" for x in rows)
        working = sum(x["working"] in {"reported_working", "verified_working"} for x in rows)
        high_quality = sum(x["working"] == "verified_working" and x["grade"] in {"A", "B"} for x in rows)
        accepted = {x["lead"] for x in rows if x["partner"] == "accepted"}
        completed = {x["lead"] for x in rows if x["pickup"] == "completed"}
        net = []
        unpriced = 0
        for row in rows:
            if row["pickup"] != "completed":
                continue
            if any(x is None for x in row["money"]):
                unpriced += 1
            else:
                price, acquisition, transport, repair, lead_fee = row["money"]
                net.append(price - acquisition - transport - repair - lead_fee)
        renewals = renewal.get(key, [])
        report.append({
            "state_code": key[0], "territory_id": key[1], "month": key[2],
            "unique_leads": len(leads), "appliance_items": len(rows),
            "reported_or_verified_working_items": working,
            "verified_working_items": verified,
            "verified_grade_a_b_items": high_quality,
            "photo_supported_items": sum(x["photos"] for x in rows),
            "partner_accepted_leads": len(accepted),
            "completed_pickup_leads": len(completed),
            "verified_working_item_rate_pct": pct(verified, len(rows)),
            "a_b_item_rate_pct": pct(high_quality, len(rows)),
            "partner_acceptance_rate_pct": pct(len(accepted), len(leads)),
            "pickup_completion_rate_pct": pct(len(completed), len(leads)),
            "items_with_realized_net_margin": len(net),
            "items_missing_realized_margin": unpriced,
            "average_realized_net_margin_cents": round(sum(net) / len(net)) if net else None,
            "total_realized_net_margin_cents": sum(net) if net else None,
            "renewal_outcomes_observed": len(renewals) if len(renewals) >= min_partners else None,
            "observed_next_month_renewal_rate_pct": (
                pct(sum(renewals), len(renewals)) if len(renewals) >= min_partners else None
            ),
            "readiness": "observations_only_not_sale_approval",
        })

    return {
        "metadata": {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "source": "private local operational CSV export, not website analytics estimates",
            "no_personal_records_exported": True,
            "min_unique_leads_for_reporting": min_leads,
            "min_partner_accounts_for_retention_rate": min_partners,
            "suppressed_small_cohorts": suppressed,
            "has_observed_rows": bool(items),
            "billing_or_territory_activation_authorized": False,
            "disclosure": "Research report only; inspect data completeness before decisions.",
        },
        "territories": report,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="PRIVATE one-appliance-per-row CSV")
    parser.add_argument("--partner-months", help="Optional PRIVATE partner monthly CSV")
    parser.add_argument("--output", required=True, help="PRIVATE aggregate-only JSON output")
    args = parser.parse_args()
    rows = read_csv(args.input, REQUIRED)
    partner_rows = read_csv(args.partner_months, PARTNER_REQUIRED) if args.partner_months else []
    report = build_report(rows, partner_rows)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(report['territories'])} aggregate territory-month cohorts; no individual records.")


if __name__ == "__main__":
    main()
