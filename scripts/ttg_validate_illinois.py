#!/usr/bin/env python3
"""TTG Illinois request-page preflight, independent of paid/limited AI reviewers.

Read only. Does not approve releases, certify local pickup service or index pages.
"""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
FORM_ACTION = "https://formspree.io/f/mvzeapzd"
SITE = "https://freereliableappliancepickup.com/"
REQUIRED = (
    "name", "phone", "address", "city", "state", "zip", "appliance",
    "condition", "floor", "stairs", "photos_available", "access", "message",
)


class Page(HTMLParser):
    """Extract only actual page tags and submitted form controls."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.forms = []
        self.form_depth = 0
        self.fields = {}
        self.state_values = []
        self.images = []
        self.robots = []
        self.canonicals = []
        self.scripts = []
        self.in_state = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "form":
            self.forms.append(attrs)
            self.form_depth += 1
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.robots.append(attrs.get("content", ""))
        if tag == "link" and "canonical" in (attrs.get("rel") or "").casefold().split():
            self.canonicals.append(attrs.get("href"))
        if tag == "img":
            self.images.append(attrs)
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])
        if tag == "select" and self.form_depth and attrs.get("name") == "state":
            self.in_state = True
        if tag == "option" and self.in_state:
            self.state_values.append(attrs.get("value"))
        if self.form_depth and tag in {"input", "textarea", "select"} and attrs.get("name"):
            self.fields.setdefault(attrs["name"], []).append(attrs)

    def handle_endtag(self, tag):
        if tag == "form" and self.form_depth:
            self.form_depth -= 1
            self.in_state = False
        if tag == "select":
            self.in_state = False


def is_illinois_page(path):
    """Limit auditing to Illinois statewide and city/category request paths."""
    slug = path.parent.name
    return slug == "illinois-appliance-pickup" or (
        "-il-" in slug and slug.endswith("-pickup")
    )


def validate(path, root=ROOT, request_only=True):
    """Return precise preflight failures for an Illinois HTML page."""
    errors = []
    path = Path(path)
    try:
        html = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"{path}: unable to read HTML ({type(exc).__name__})"]
    parsed = Page()
    parsed.feed(html)
    slug = path.parent.name
    if parsed.h1 != 1:
        errors.append("expected one primary H1")
    if len(parsed.canonicals) != 1 or parsed.canonicals[0] != SITE + slug + "/":
        errors.append("incorrect or duplicate self-canonical")
    if request_only:
        directives = (
            {s.strip().casefold() for s in parsed.robots[0].split(",")}
            if len(parsed.robots) == 1 else set()
        )
        if not {"noindex", "follow"} <= directives or "index" in directives or "nofollow" in directives:
            errors.append("unconfirmed Illinois market must be noindex, follow")
    if len(parsed.forms) != 1 or parsed.forms[0].get("action") != FORM_ACTION:
        errors.append("expected one known Formspree intake form")
    elif parsed.forms[0].get("method", "").casefold() != "post":
        errors.append("intake form must use POST")
    if "/assets/customer-routing.js" not in parsed.scripts:
        errors.append("customer-routing.js missing")
    for name in REQUIRED:
        fields = parsed.fields.get(name, [])
        if len(fields) != 1:
            errors.append(f"missing or duplicate field: {name}")
        elif "required" not in fields[0]:
            errors.append(f"required customer field not enforced: {name}")
    if parsed.state_values != ["", "IL"]:
        errors.append("pickup state must be restricted to Illinois")
    source_fields = parsed.fields.get("source_page", [])
    if len(source_fields) != 1 or source_fields[0].get("value") != slug:
        errors.append("missing or mismatched source_page tag")
    if not parsed.fields.get("paid_option"):
        errors.append("separate voluntary paid quote option missing")
    if not parsed.fields.get("privacy_acknowledgment") and "/privacy/" not in html:
        errors.append("privacy disclosure missing")
    if len(parsed.images) != 1:
        errors.append("expected exactly one real appliance photo")
    for img in parsed.images:
        src = img.get("src", "")
        alt = (img.get("alt") or "").strip()
        if len(alt) < 15:
            errors.append("image needs meaningful descriptive alt text")
        p = urlsplit(src)
        if p.scheme or p.netloc or not src.startswith("/"):
            errors.append("photo must be a local verified image path")
            continue
        asset = (root / p.path.lstrip("/")).resolve()
        if not asset.is_relative_to(root.resolve()) or not asset.is_file():
            errors.append(f"photo missing from repository: {src}")
    if "guaranteed free pickup" in html.casefold():
        errors.append("unsupported unconditional free pickup claim")
    return [f"{path}: {e}" for e in errors]


def main():
    """Audit all Illinois files present in this checkout without publishing."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    routing = json.loads((ROOT / "data/market-routing.json").read_text(encoding="utf-8"))
    state = next(x for x in routing["state_defaults"] if x["state_code"] == "IL")
    request_only = state["status"] == "request-only"
    if not request_only:
        print("Illinois route status changed: verify actual coverage before altering index controls.", file=sys.stderr)
        return 1
    paths = args.paths or sorted([
        ROOT / "illinois-appliance-pickup" / "index.html",
        *ROOT.glob("*-il-*-pickup/index.html"),
    ])
    paths = [p for p in paths if p.exists() and is_illinois_page(p)]
    errors = []
    for path in paths:
        errors.extend(validate(path, ROOT, request_only=request_only))
    print(f"TTG Illinois: checked {len(paths)} HTML pages; {len(errors)} preflight errors.")
    for err in errors:
        print(err, file=sys.stderr)
    if not paths:
        print("No Illinois request pages in this branch (validator itself still unit-tested).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
