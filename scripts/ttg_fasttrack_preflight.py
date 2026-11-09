#!/usr/bin/env python3
"""FastTrack read-only page preflight: form, image, canonical, and indexing checks.

Example: python scripts/ttg_fasttrack_preflight.py --state IL
         python scripts/ttg_fasttrack_preflight.py --path chicago-il-appliance-pickup/index.html --state IL

Checks checked-out files only. Passing does not verify actual HTTP, deployed pages,
a successful Formspree submission, operator coverage or Google index eligibility.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from scripts.ttg_fasttrack_inventory import ROOT, collect, load_sources, slugify

REQUIRED_FIELDS = frozenset(
    ("name", "phone", "address", "city", "state", "zip",
     "appliance", "condition", "floor", "stairs", "access", "photos_available")
)
EXPECTED_FORM_ACTION = "https://formspree.io/f/mvzeapzd"
CANONICAL_HOST = "freereliableappliancepickup.com"


class HTMLFacts(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.forms: list[dict] = []
        self.images: list[dict] = []
        self.fields: dict[str, list[dict]] = {}
        self.canonicals: list[str] = []
        self.robots: list[str] = []
        self.h1_count = 0
        self.title_count = 0
        self._in_title = False
        self.title_text: list[str] = []
        self.visible_text: list[str] = []

    def handle_starttag(self, tag: str, pairs: list[tuple[str, str | None]]) -> None:
        attrs = dict(pairs)
        if tag == "form":
            self.forms.append(attrs)
        elif tag == "img":
            self.images.append(attrs)
        elif tag in ("input", "select", "textarea") and attrs.get("name"):
            self.fields.setdefault(attrs["name"], []).append(attrs)
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self.title_count += 1
            self._in_title = True
        elif tag == "link" and "canonical" in (attrs.get("rel") or "").split():
            self.canonicals.append(attrs.get("href") or "")
        elif tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.robots.append(attrs.get("content") or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_text.append(data)
        self.visible_text.append(data)


def clean_relpath(root: Path, value: str) -> Path:
    file_path = (root / value).resolve()
    if not file_path.is_relative_to(root.resolve()):
        raise ValueError("Requested path escapes repository checkout")
    if file_path.name != "index.html":
        raise ValueError("Expected a page's index.html")
    return file_path


def inspect_page(root: Path, path: str, state_code: str, *, request_only: bool) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        file_path = clean_relpath(root, path)
        markup = file_path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        return {"path": path, "errors": ["unreadable_or_invalid_path: " + str(exc)],
                "warnings": [], "passed": False}
    facts = HTMLFacts()
    facts.feed(markup)
    if len(facts.forms) != 1 or facts.forms[0].get("action") != EXPECTED_FORM_ACTION:
        errors.append("expected_exactly_one_existing_formspree_form")
    missing = sorted(REQUIRED_FIELDS.difference(facts.fields))
    if missing:
        errors.append("required_fields_missing:" + ",".join(missing))
    for name in sorted(REQUIRED_FIELDS.intersection(facts.fields)):
        if not any("required" in f for f in facts.fields[name]):
            errors.append("required_attribute_missing:" + name)
    if len(facts.images) != 1:
        errors.append("expected_one_real_appliance_image")
    for image in facts.images:
        src = image.get("src", "")
        if not src or src.startswith(("http://", "https://", "//", "data:")):
            errors.append("image_must_use_existing_local_asset")
            continue
        asset_path = (root / src.lstrip("/").split("?")[0]).resolve()
        if not asset_path.is_relative_to(root.resolve()) or not asset_path.is_file():
            errors.append("image_asset_not_found:" + src)
        if not (image.get("alt") or "").strip():
            errors.append("image_alt_missing")
    if facts.h1_count != 1 or facts.title_count != 1 or not "".join(facts.title_text).strip():
        errors.append("expected_one_h1_and_one_nonempty_title")
    if len(facts.canonicals) != 1:
        errors.append("expected_one_self_canonical")
    else:
        url = urlparse(facts.canonicals[0])
        expected = "/" + str(file_path.parent.relative_to(root.resolve())).replace("\\", "/") + "/"
        if url.scheme != "https" or url.netloc != CANONICAL_HOST or url.path != expected:
            errors.append("canonical_mismatch:" + facts.canonicals[0])
    if request_only and not any("noindex" in value.lower() for value in facts.robots):
        errors.append("request_only_must_be_noindex")
    if "source_page" not in facts.fields:
        errors.append("source_page_missing")
    if "privacy_acknowledgment" not in facts.fields:
        warnings.append("privacy_acknowledgment_not_detected")
    if "photo_link" not in facts.fields:
        warnings.append("no_photo_url_or_native_upload_assessed")
    state_field = facts.fields.get("state", [])
    if state_field and state_code not in markup:
        # Basic source check only: option-value semantics need browser-level validation.
        warnings.append("state_code_not_visible_in_html_source")
    text = " ".join(facts.visible_text).lower()
    if request_only and not any(x in text for x in
                                ("not guaranteed", "not confirmed", "request-only",
                                 "request only", "eligibility review", "no active")):
        errors.append("unverified_market_must_disclose_coverage")
    if "customer-routing.js" not in markup:
        warnings.append("shared_customer_routing_not_linked")
    return {"path": path, "state_code": state_code, "errors": errors, "warnings": warnings,
            "passed": not errors, "publication_approved": False,
            "note": "Static source preflight only; independent review, deployment, form and service checks remain."}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--state", required=True, help="State name or code; never inferred from ambiguous file names")
    parser.add_argument("--path", action="append", help="Explicit repo-relative index.html (may repeat)")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--output", type=Path, help="Write machine-readable JSON report")
    args = parser.parse_args(argv)
    if args.limit < 0:
        parser.error("limit cannot be negative")
    routing, _ = load_sources(args.root)
    states = {s["state_code"]: s["state"] for s in routing["state_defaults"]}
    wanted = args.state.strip().casefold()
    code = next((c for c, name in states.items()
                 if wanted in (c.casefold(), name.casefold())), None)
    if not code:
        parser.error("Unknown state")
    default = next(s for s in routing["state_defaults"] if s["state_code"] == code)
    if args.path:
        candidates = [(x, default.get("status") not in ("direct", "partner-supported"))
                      for x in args.path]
    else:
        _, cities = collect(args.root)
        candidates = []
        for city in cities:
            if city["state_code"] != code:
                continue
            for page in city["page_slots"].values():
                # Never auto-attribute legacy unscoped filenames to a city/state.
                if page["source"] == "state-scoped":
                    candidates.append(
                        (page["file"],
                         city["routing_status"] not in ("direct", "partner-supported")))
        candidates = sorted(set(candidates))
    if args.limit:
        candidates = candidates[:args.limit]
    if not candidates:
        report = {"state_code": code, "checked": 0, "passed": 0, "failed": 0,
                  "results": [], "note": "No eligible files in this checkout; NOT a pass"}
        exit_code = 2
    else:
        results = [inspect_page(args.root, p, code, request_only=ro) for p, ro in candidates]
        failed = sum(not x["passed"] for x in results)
        report = {"state_code": code, "checked": len(results),
                  "passed": len(results) - failed, "failed": failed, "results": results,
                  "publication_approved": False}
        exit_code = 1 if failed else 0
    output = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
