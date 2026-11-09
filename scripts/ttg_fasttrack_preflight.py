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

# Support direct `python scripts/ttg_fasttrack_preflight.py` as well as unittest imports.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
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
        self._in_form = False
        self._in_state_select = False
        self._state_option_value: str | None = None
        self._state_option_text: list[str] | None = None
        self.state_options: set[str] = set()
        self.title_text: list[str] = []
        self.visible_text: list[str] = []

    def handle_starttag(self, tag: str, pairs: list[tuple[str, str | None]]) -> None:
        attrs = dict(pairs)
        if tag == "form":
            self.forms.append(attrs)
            self._in_form = True
        elif tag == "img":
            self.images.append(attrs)
        elif tag in ("input", "select", "textarea") and self._in_form and attrs.get("name"):
            self.fields.setdefault(attrs["name"], []).append(attrs)
            if tag == "select" and attrs["name"] == "state":
                self._in_state_select = True
        elif tag == "option" and self._in_state_select:
            # An option with no value submits its visible text as its value.
            self._state_option_value = attrs.get("value")
            self._state_option_text = []
            if self._state_option_value is not None:
                self.state_options.add(self._state_option_value)
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
        elif tag == "form":
            self._in_form = False
        elif tag == "option" and self._state_option_text is not None:
            if self._state_option_value is None:
                self.state_options.add("".join(self._state_option_text))
            self._state_option_value = None
            self._state_option_text = None
        elif tag == "select":
            self._in_state_select = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_text.append(data)
        if self._state_option_text is not None:
            self._state_option_text.append(data)
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
    if len(facts.forms) == 1 and facts.forms[0].get("method", "").strip().lower() != "post":
        # GET would expose a customer's phone and street address in URL/query logs.
        errors.append("form_must_use_post")
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
    source_fields = facts.fields.get("source_page", [])
    if len(source_fields) != 1 or not (source_fields[0].get("value") or "").strip():
        errors.append("source_page_missing_or_empty")
    elif source_fields[0].get("value", "").strip() != file_path.parent.name:
        # Duplicate or misattributed identifiers would corrupt city-level lead data.
        errors.append("source_page_mismatch")
    privacy_fields = facts.fields.get("privacy_acknowledgment", [])
    if (len(privacy_fields) != 1
            or "required" not in privacy_fields[0]
            or privacy_fields[0].get("type", "").lower() != "checkbox"):
        errors.append("privacy_acknowledgment_must_be_required")
    if "photo_link" not in facts.fields:
        warnings.append("no_photo_url_or_native_upload_assessed")
    state_field = facts.fields.get("state", [])
    values = {str(f.get("value") or "").strip().upper() for f in state_field}
    values.update(x.strip().upper() for x in facts.state_options)
    # A selector accepting IL *and* another state is not an IL-only intake form.
    allowed_values = values - {""}
    if allowed_values != {state_code.upper()}:
        errors.append("form_state_must_be_restricted_to_target_code")
    text = " ".join(facts.visible_text).lower()
    if request_only and not any(x in text for x in
                                ("not guaranteed", "not confirmed", "request-only",
                                 "request only", "eligibility review", "no active")):
        errors.append("unverified_market_must_disclose_coverage")
    # A native async submit handler + the shared capture-phase router can queue
    # duplicate requestSubmit() events while routing metadata is loading.
    # Require a document-capture guard before approving this staged source.
    async_handler = any(fragment in markup for fragment in (
        "form.addEventListener('submit', async",
        'form.addEventListener("submit", async',
        "form.addEventListener('submit',async",
        'form.addEventListener("submit",async',
    ))
    if async_handler and "customer-routing.js" in markup:
        markers = (
            "document.addEventListener('submit'",
            "routingPending",
            "event.stopImmediatePropagation()",
            "form.dataset.customerRoutingQualified",
        )
        if not all(marker in markup for marker in markers):
            errors.append("async_routing_duplicate_submit_guard_missing")
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
