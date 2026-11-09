#!/usr/bin/env python3
"""Offline TTG FastTrack batch preflight. Not a production release approval."""
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
FORM = "https://formspree.io/f/mvzeapzd"
SITE = "https://freereliableappliancepickup.com/"
REQUIRED = ("name", "phone", "address", "city", "state", "zip", "appliance",
            "condition", "floor", "stairs", "photos_available", "access", "message")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.form_depth = 0
        self.forms, self.fields, self.images = [], {}, []
        self.robots, self.canonicals, self.scripts = [], [], []
        self.state_options = []
        self.in_state = False

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag == "h1":
            self.h1 += 1
        if tag == "meta" and (a.get("name") or "").lower() == "robots":
            self.robots.append(a.get("content", ""))
        if tag == "link" and "canonical" in (a.get("rel") or "").lower().split():
            self.canonicals.append(a.get("href"))
        if tag == "img":
            self.images.append(a)
        if tag == "script" and a.get("src"):
            self.scripts.append(a["src"])
        if tag == "form":
            self.forms.append(a)
            self.form_depth += 1
        if tag == "select" and self.form_depth and a.get("name") == "state":
            self.in_state = True
        if tag == "option" and self.in_state:
            self.state_options.append(a.get("value"))
        if self.form_depth and tag in {"input", "select", "textarea"} and a.get("name"):
            self.fields.setdefault(a["name"], []).append(a)

    def handle_endtag(self, tag):
        if tag == "select":
            self.in_state = False
        if tag == "form" and self.form_depth:
            self.form_depth -= 1
            self.in_state = False


def check_page(path, root, code):
    failures = []
    parsed = Page()
    html = path.read_text(encoding="utf-8")
    parsed.feed(html)
    slug = path.parent.name
    if parsed.h1 != 1:
        failures.append("expected exactly one H1")
    if parsed.canonicals != [SITE + slug + "/"]:
        failures.append("missing or incorrect self-canonical")
    directives = set()
    if len(parsed.robots) == 1:
        directives = {v.strip().lower() for v in parsed.robots[0].split(",")}
    if not {"noindex", "follow"} <= directives or {"index", "nofollow"} & directives:
        failures.append("unverified pickup page must be noindex, follow")
    if len(parsed.forms) != 1 or parsed.forms[0].get("action") != FORM or (
        parsed.forms[0].get("method") or ""
    ).lower() != "post":
        failures.append("expected one POST to the established Formspree endpoint")
    if "/assets/customer-routing.js" not in parsed.scripts:
        failures.append("missing customer routing script")
    for name in REQUIRED:
        fields = parsed.fields.get(name, [])
        if len(fields) != 1 or "required" not in fields[0]:
            failures.append("missing, duplicate or optional required input: " + name)
    if parsed.state_options != ["", code]:
        failures.append("pickup state options must be blank and " + code)
    sources = parsed.fields.get("source_page", [])
    if len(sources) != 1 or sources[0].get("value") != slug:
        failures.append("source_page must match directory slug")
    if not parsed.fields.get("paid_option"):
        failures.append("missing separate optional paid quote preference")
    if "/privacy/" not in html:
        failures.append("missing first-party privacy disclosure link")
    if len(parsed.images) != 1:
        failures.append("expected one actual appliance image element")
    for img in parsed.images:
        src = img.get("src") or ""
        if len((img.get("alt") or "").strip()) < 15:
            failures.append("image needs meaningful alt text")
        url = urlsplit(src)
        if url.scheme or url.netloc or not src.startswith("/"):
            failures.append("image must have a local absolute path")
        else:
            photo = (root / url.path.lstrip("/")).resolve()
            if not photo.is_relative_to(root.resolve()) or not photo.is_file():
                failures.append("image asset does not exist: " + src)
    if "guaranteed free pickup" in html.casefold():
        failures.append("unsupported guaranteed pickup claim")
    return failures


def check_manifest(path, root=ROOT):
    problems = []
    try:
        batch = json.loads(path.read_text(encoding="utf-8"))
        code, pages = batch["state_code"], batch["pages"]
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        return [f"{path}: invalid batch manifest: {exc}"]
    if not isinstance(code, str) or not re.fullmatch(r"[A-Z]{2}", code):
        return [f"{path}: state_code must be two uppercase letters"]
    if path.stem != code:
        problems.append("manifest must be named STATE.json")
    if batch.get("mode") != "request-only":
        problems.append("only request-only staging supported; activation requires approval")
    state_slug = ""
    try:
        routing = json.loads((root / "data/market-routing.json").read_text(encoding="utf-8"))
        rows = [row for row in routing["state_defaults"] if row["state_code"] == code]
        if len(rows) != 1:
            problems.append("expected exactly one routing default")
        else:
            state_slug = rows[0].get("state", "").strip().lower().replace(" ", "-") + "-appliance-pickup"
            if rows[0]["status"] not in {"request-only", "partner-recruiting"}:
                problems.append("routing changed: independently verify coverage")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        problems.append(f"unable to check market routing: {exc}")
    if not isinstance(pages, list) or not pages:
        return [f"{path}: pages must be a nonempty list", *problems]
    seen = set()
    for raw in pages:
        if not isinstance(raw, str) or raw in seen:
            problems.append("page paths must be unique strings")
            continue
        seen.add(raw)
        rel = Path(raw)
        if rel.is_absolute() or ".." in rel.parts or rel.name != "index.html":
            problems.append("unsafe page path: " + raw)
            continue
        slug = rel.parent.name
        intents = ("appliance", "washer-dryer", "refrigerator", "freezer",
                   "stove-oven", "stove", "washer", "dryer")
        valid_city = any(slug.endswith(f"-{code.lower()}-{intent}-pickup")
                         and len(slug) > len(f"-{code.lower()}-{intent}-pickup")
                         for intent in intents)
        if slug != state_slug and not valid_city:
            problems.append("wrong state-coded pickup directory: " + raw)
            continue
        page = (root / rel).resolve()
        if not page.is_relative_to(root.resolve()) or not page.is_file():
            problems.append("page missing from checkout: " + raw)
            continue
        try:
            problems.extend(f"{raw}: {e}" for e in check_page(page, root, code))
        except (OSError, UnicodeError, ValueError) as exc:
            problems.append(f"{raw}: unable to inspect HTML: {exc}")
    return [f"{path}: {p}" for p in problems]


def main():
    manifests = sorted((ROOT / "data/ttg-state-batches").glob("*.json"))
    if not manifests:
        print("No TTG state manifest in this checkout. QA engine only; NO pages approved.")
        return 0
    problems = [error for manifest in manifests for error in check_manifest(manifest)]
    print(f"TTG batch preflight: {len(manifests)} manifests, {len(problems)} errors; NOT an approval.")
    for error in problems:
        print(error, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
