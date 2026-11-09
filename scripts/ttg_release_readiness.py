#!/usr/bin/env python3
"""TTG FastTrack state readiness: staged-code health versus verified fulfillment.

Quota-free and read-only. Never submits customer forms, verifies a provider
identity, changes robots directives, or promotes unserved cities into search.
"""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

from scripts.ttg_state_batch_qa import ROOT, check_manifest


def staged_cities(pages, state_code):
    """Return owner-city slugs, not category variations or the statewide hub."""
    suffix = "-" + state_code.lower() + "-appliance-pickup/index.html"
    return sorted({p[:-len(suffix)] for p in pages if p.endswith(suffix) and p[:-len(suffix)]})


def dated(value):
    """Require an actual calendar date without implying it was independently verified."""
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def evidence_check(record, cities, requested_city=None):
    """Return recorded operational prerequisites; evidence still needs human review."""
    errors = []
    if not isinstance(record, dict):
        return [], ["missing or invalid readiness ledger"]
    receipt = record.get("form_receipt", {})
    if not isinstance(receipt, dict) or not (
        receipt.get("verified") is True
        and dated(receipt.get("verified_on"))
        and isinstance(receipt.get("receipt_reference"), str)
        and receipt["receipt_reference"].strip()
    ):
        errors.append("Owner-controlled Formspree test receipt has not been documented")
    approval = record.get("owner_release_approval", {})
    if not isinstance(approval, dict) or not (
        approval.get("approved") is True
        and dated(approval.get("approved_on"))
        and isinstance(approval.get("reference"), str)
        and approval["reference"].strip()
    ):
        errors.append("Owner/maintainer operational activation approval is not documented")
    entries = record.get("verified_cities", [])
    if not isinstance(entries, list):
        entries = []
        errors.append("verified_cities must be a list")
    seen = set()
    verified = []
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("Malformed city evidence")
            continue
        city = entry.get("city_slug")
        if city not in cities:
            errors.append("Unknown city evidence: " + str(city))
            continue
        if city in seen:
            errors.append("Duplicate city evidence: " + city)
            continue
        seen.add(city)
        zip_codes = entry.get("zip_codes", [])
        if not (
            isinstance(zip_codes, list) and zip_codes and
            all(isinstance(z, str) and re.fullmatch(r"\d{5}", z) for z in zip_codes)
            and isinstance(entry.get("operator_reference"), str)
            and entry["operator_reference"].strip()
            and entry.get("pickup_terms_checked") is True
            and dated(entry.get("verified_on"))
        ):
            errors.append("Incomplete ZIP/operator/terms evidence for " + city)
            continue
        verified.append(city)
    target = [requested_city] if requested_city else cities
    for city in target:
        if city not in verified:
            errors.append("No recorded accepting operator, ZIP coverage and terms for " + city)
    return sorted(verified), errors


def assess(state_code, root=ROOT, city=None):
    """Evaluate staged HTML independently from the separate evidence ledger."""
    state_code = state_code.upper()
    manifest = root / "data/ttg-state-batches" / (state_code + ".json")
    evidence = root / "data/ttg-release-readiness" / (state_code + ".json")
    technical = []
    if not manifest.is_file():
        return {"state": state_code, "technical_errors": ["No state batch manifest"], "operational_blockers": [],
                "pages": 0, "cities": [], "verified_cities": [], "request_only_safe": False,
                "operational_prerequisites_recorded": False, "index_activation_authorized": False}
    try:
        batch = json.loads(manifest.read_text(encoding="utf-8"))
        pages = batch["pages"]
        if not isinstance(pages, list):
            raise ValueError("pages must be a list")
        cities = staged_cities(pages, state_code)
        technical.extend(check_manifest(manifest, root))
        if batch.get("mode") != "request-only":
            technical.append("FastTrack readiness supports only request-only batches")
        routing = json.loads((root / "data/market-routing.json").read_text(encoding="utf-8"))
        defaults = [r for r in routing["state_defaults"] if r.get("state_code") == state_code]
        if len(defaults) != 1 or defaults[0].get("status") != "request-only":
            technical.append("Staging route must remain request-only until independent operational verification")
        if not cities:
            technical.append("No staged owner-city pages found")
        if city and city not in cities:
            technical.append("Requested city is not in the stage manifest: " + city)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return {"state": state_code, "technical_errors": [str(exc)], "operational_blockers": [],
                "pages": 0, "cities": [], "verified_cities": [], "request_only_safe": False,
                "operational_prerequisites_recorded": False, "index_activation_authorized": False}
    try:
        ledger = json.loads(evidence.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        ledger = {}
        technical.append("Missing or unreadable operational evidence ledger: " + type(exc).__name__)
    if ledger.get("state_code") != state_code:
        technical.append("Readiness ledger state_code does not match batch")
    verified, blockers = evidence_check(ledger, cities, city)
    staged_safe = not technical
    return {
        "state": state_code, "pages": len(pages), "cities": cities,
        "verified_cities": verified, "technical_errors": technical,
        "operational_blockers": blockers, "request_only_safe": staged_safe,
        "operational_prerequisites_recorded": staged_safe and not blockers,
        # The separate, approved index-activation PR is intentionally never automated.
        "index_activation_authorized": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, help="Two-letter state code, e.g. IL")
    parser.add_argument("--city", help="Optional city slug for city-specific operational evidence")
    parser.add_argument("--report", type=Path, help="Write the machine-readable readiness report")
    parser.add_argument("--require-evidence", action="store_true",
                        help="Fail until the operational proof prerequisites are recorded")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Z]{2}", args.state.upper()):
        parser.error("state must be two letters")
    result = assess(args.state, city=args.city)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"TTG {result['state']}: {result['pages']} staged request pages, "
          f"{len(result['cities'])} cities, {len(result['verified_cities'])} cities with evidence.")
    for problem in result["technical_errors"]:
        print("TECHNICAL:", problem, file=sys.stderr)
    for blocker in result["operational_blockers"]:
        print("NOT OPERATIONALLY VERIFIED:", blocker)
    print("Staged technical safety:", "PASS" if result["request_only_safe"] else "FAIL")
    print("Operational evidence:", "RECORDED" if result["operational_prerequisites_recorded"]
          else "INCOMPLETE")
    print("Google indexing activation: NOT AUTHORIZED — separate verified city release required.")
    return int(bool(result["technical_errors"] or
                    (args.require_evidence and result["operational_blockers"])))


if __name__ == "__main__":
    sys.exit(main())
