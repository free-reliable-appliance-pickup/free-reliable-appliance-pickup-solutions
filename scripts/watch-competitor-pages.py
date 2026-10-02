#!/usr/bin/env python3
"""Watch priority competitor pages for meaningful SEO/conversion changes.

Stdlib-only so it can run for free in GitHub Actions. The watcher compares
competitor structure with our intended owner page and emits an actionable
battle report rather than a generic "page changed" alert.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (compatible; FreeReliableAppliancePickup-CompetitorWatch/1.0; +https://freereliableappliancepickup.com/)"
TIMEOUT = 25

SIGNAL_TERMS = {
    "photo_first": ("photo", "photos", "picture"),
    "access_detail": ("stairs", "elevator", "gate", "garage", "driveway", "tight", "basement", "access"),
    "trust_flow": ("free to submit", "no account", "request is", "not a confirmed", "confirm pickup", "confirms the pickup"),
    "commercial_recurring": ("commercial", "business appliance", "property manager", "recurring", "apartment", "senior", "55+"),
    "local_specificity": ("zip code", "zip codes", "neighborhood", "county", "local details", "service areas"),
    "local_fallback": ("city of ", "public works", "solid waste", "burrtec", "waste management", "republic services", "landfill", "bulky"),
    "faq": ("frequently asked questions", "faq"),
}
AGGRESSIVE_TERMS = (
    "100% free", "no hidden fees", "any condition", "working or broken",
    "zero cost", "no cost ever", "same-day", "same day",
    "no charge for stairs", "regardless of their condition",
)
APPLIANCE_SLUG_TERMS = (
    "refrigerator", "washer", "washing-machine", "dryer", "dishwasher",
    "oven", "stove", "microwave", "freezer", "water-heater",
)
COUNTERMOVES = {
    "photo_first": "Add or strengthen a photo-first request path only if the current owner page lacks it.",
    "access_detail": "Add practical stairs/elevator/gate/garage/doorway access guidance; do not add filler.",
    "trust_flow": "Clarify free-to-submit/no-account/confirmation language without promising an unconfirmed appointment.",
    "commercial_recurring": "Add a truthful property-manager, apartment, senior/55+, hotel or recurring-program path where service really supports it.",
    "local_specificity": "Add useful city-specific ZIP/neighborhood/access/route detail from reliable sources; avoid city-name swaps.",
    "local_fallback": "Add an official municipal/hauler alternative for requests that do not qualify.",
    "faq": "Add real customer questions and matching FAQPage schema only when answers are useful and accurate.",
    "appliance_depth": "Link to useful appliance-specific guides from the city owner page; do not mass-create thin city×appliance pages.",
    "aggressive_guarantee": "Do not copy unverified blanket guarantees. Keep qualification, access, timing and partner/route limits explicit.",
}

class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts = []
        self.h1_parts = []
        self.visible_parts = []
        self.links = []
        self.meta_description = ""
        self.robots = ""
        self.canonical = ""
        self.jsonld_chunks = []
        self._in_title = False
        self._in_h1 = False
        self._jsonld = False
        self._json_buf = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        a = {str(k).lower(): (v or "") for k, v in attrs}
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
        elif tag == "meta":
            name = a.get("name", "").lower()
            prop = a.get("property", "").lower()
            if name == "description" and not self.meta_description:
                self.meta_description = a.get("content", "")
            if name == "robots" and not self.robots:
                self.robots = a.get("content", "")
            if prop == "og:description" and not self.meta_description:
                self.meta_description = a.get("content", "")
        elif tag == "link":
            rel = a.get("rel", "").lower()
            if "canonical" in rel and not self.canonical:
                self.canonical = a.get("href", "")
        elif tag == "a":
            href = a.get("href", "").strip()
            if href:
                self.links.append(href)
        elif tag == "script":
            if "ld+json" in a.get("type", "").lower():
                self._jsonld = True
                self._json_buf = []
            else:
                self._skip += 1
        elif tag == "style":
            self._skip += 1

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "script":
            if self._jsonld:
                self.jsonld_chunks.append("".join(self._json_buf))
                self._jsonld = False
                self._json_buf = []
            elif self._skip:
                self._skip -= 1
        elif tag == "style" and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        if self._in_h1:
            self.h1_parts.append(data)
        if self._jsonld:
            self._json_buf.append(data)
        elif not self._skip:
            self.visible_parts.append(data)

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()

def schema_types(chunks):
    types = set()
    def walk(x):
        if isinstance(x, dict):
            t = x.get("@type")
            if isinstance(t, str):
                types.add(t)
            elif isinstance(t, list):
                types.update(str(v) for v in t)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    for chunk in chunks:
        try:
            walk(json.loads(chunk))
        except Exception:
            pass
    return sorted(types)

def important_internal_links(base_url: str, hrefs):
    base = urlparse(base_url)
    paths = set()
    for href in hrefs:
        try:
            absolute = urljoin(base_url, href)
            p = urlparse(absolute)
        except Exception:
            continue
        if p.scheme not in {"http", "https"} or p.netloc.lower() != base.netloc.lower():
            continue
        path = re.sub(r"/+", "/", p.path or "/").rstrip("/") or "/"
        low = path.lower()
        if any(term in low for term in APPLIANCE_SLUG_TERMS) or any(term in low for term in ("commercial", "locations", "recycling", "removal", "disposal")):
            paths.add(path)
    return sorted(paths)[:120]

def signals_for(text: str, important_links):
    low = text.lower()
    sig = {k: any(term in low for term in terms) for k, terms in SIGNAL_TERMS.items()}
    sig["appliance_depth"] = any(any(term in link.lower() for term in APPLIANCE_SLUG_TERMS) for link in important_links)
    sig["aggressive_guarantee"] = any(term in low for term in AGGRESSIVE_TERMS)
    return sig

def parse_html(html: str, base_url: str):
    parser = Extractor()
    parser.feed(html)
    text = norm(" ".join(parser.visible_parts))
    links = important_internal_links(base_url, parser.links)
    snap = {
        "title": norm(" ".join(parser.title_parts)),
        "meta_description": norm(parser.meta_description),
        "h1": norm(" ".join(parser.h1_parts)),
        "canonical": norm(parser.canonical),
        "robots": norm(parser.robots),
        "schema_types": schema_types(parser.jsonld_chunks),
        "important_internal_links": links,
        "important_internal_link_count": len(links),
        "word_count": len(text.split()),
        "signals": signals_for(text, links),
    }
    fingerprint_basis = {k: snap[k] for k in (
        "title", "meta_description", "h1", "canonical", "robots",
        "schema_types", "important_internal_links", "signals",
    )}
    snap["fingerprint"] = hashlib.sha256(
        json.dumps(fingerprint_basis, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return snap

def fetch(url: str):
    req = Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",
    })
    with urlopen(req, timeout=TIMEOUT) as r:
        status = getattr(r, "status", 200)
        final_url = r.geturl()
        content_type = r.headers.get("Content-Type", "")
        raw = r.read(3_000_000)
    charset = "utf-8"
    m = re.search(r"charset=([\w.-]+)", content_type, re.I)
    if m:
        charset = m.group(1)
    html = raw.decode(charset, errors="replace")
    return status, final_url, html

def local_snapshot(path: str):
    p = Path(path)
    if not p.is_file():
        return None
    return parse_html(p.read_text(encoding="utf-8", errors="replace"), "https://freereliableappliancepickup.com/" + p.parent.as_posix().strip("/") + "/")

def compare(old, new):
    if not old:
        return []
    changes = []
    for field in ("title", "meta_description", "h1", "canonical", "robots", "schema_types"):
        if old.get(field) != new.get(field):
            changes.append({"field": field, "before": old.get(field), "after": new.get(field)})
    old_sig, new_sig = old.get("signals", {}), new.get("signals", {})
    for key in sorted(set(old_sig) | set(new_sig)):
        if old_sig.get(key) != new_sig.get(key):
            changes.append({"field": f"signal:{key}", "before": old_sig.get(key), "after": new_sig.get(key)})
    old_links = set(old.get("important_internal_links", []))
    new_links = set(new.get("important_internal_links", []))
    added, removed = sorted(new_links-old_links), sorted(old_links-new_links)
    if added:
        changes.append({"field": "important_links_added", "before": [], "after": added[:12]})
    if removed:
        changes.append({"field": "important_links_removed", "before": removed[:12], "after": []})
    ow, nw = int(old.get("word_count") or 0), int(new.get("word_count") or 0)
    if ow >= 200 and abs(nw-ow)/ow >= 0.18:
        changes.append({"field": "content_size", "before": ow, "after": nw})
    return changes

def describe_changes(changes):
    parts = []
    for ch in changes:
        f = ch["field"]
        if f.startswith("signal:"):
            key = f.split(":", 1)[1]
            parts.append(f"{key} changed {ch['before']} → {ch['after']}")
        elif f == "important_links_added":
            parts.append("new important internal links: " + ", ".join(ch["after"][:6]))
        elif f == "important_links_removed":
            parts.append("important internal links removed: " + ", ".join(ch["before"][:6]))
        elif f == "content_size":
            parts.append(f"page size changed from about {ch['before']} to {ch['after']} words")
        else:
            before = norm(str(ch["before"]))[:120]
            after = norm(str(ch["after"]))[:120]
            parts.append(f"{f} changed: {before!r} → {after!r}")
    return "; ".join(parts)

def strengths(sig):
    friendly = {
        "photo_first":"photo-first intake", "access_detail":"access detail",
        "trust_flow":"confirmation/trust flow", "commercial_recurring":"commercial/recurring coverage",
        "local_specificity":"local ZIP/neighborhood detail", "local_fallback":"official local fallback",
        "faq":"FAQ coverage", "appliance_depth":"appliance-specific guide depth",
    }
    return [friendly[k] for k in friendly if sig.get(k)]

def choose_counter(new, ours, changes):
    ns = new.get("signals", {})
    osig = (ours or {}).get("signals", {})
    gaps = [k for k in COUNTERMOVES if k != "aggressive_guarantee" and ns.get(k) and not osig.get(k)]
    notes = []
    if ns.get("aggressive_guarantee") and not osig.get("aggressive_guarantee"):
        notes.append(COUNTERMOVES["aggressive_guarantee"])
    for gap in gaps:
        notes.append(COUNTERMOVES[gap])
    if any(ch["field"] == "important_links_added" for ch in changes) and not osig.get("appliance_depth"):
        notes.append(COUNTERMOVES["appliance_depth"])
    if not notes:
        notes.append("PROTECT: our owner page already covers the main benchmark signals. Inspect the exact live query before changing title, copy or architecture.")
    return gaps, notes

def set_output(name, value):
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"{name}={value}\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="data/competitor-watch-targets.json")
    ap.add_argument("--baseline", default="data/competitor-watch-snapshots.json")
    ap.add_argument("--report", default="reports/competitor-watch-latest.md")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    baseline_path = Path(args.baseline)
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    baseline = {}
    if baseline_path.exists():
        try:
            baseline = json.loads(baseline_path.read_text(encoding="utf-8")).get("snapshots", {})
        except Exception:
            baseline = {}

    seeded = not bool(baseline)
    next_baseline = dict(baseline)
    alerts = []
    errors = []
    successes = 0

    for target in config.get("targets", []):
        tid = target["id"]
        try:
            status, final_url, html = fetch(target["url"])
            if status >= 400:
                raise RuntimeError(f"HTTP {status}")
            current = parse_html(html, final_url)
            current["final_url"] = final_url
            successes += 1
        except Exception as exc:
            errors.append(f"{tid}: {type(exc).__name__}: {exc}")
            continue

        old = baseline.get(tid)
        changes = compare(old, current)
        next_baseline[tid] = current

        if old and changes:
            ours = local_snapshot(target.get("our_path", ""))
            gaps, countermoves = choose_counter(current, ours, changes)
            alerts.append({
                "target": target,
                "changes": changes,
                "current": current,
                "ours": ours,
                "gaps": gaps,
                "countermoves": countermoves,
            })

    if successes == 0:
        print("ERROR: no competitor pages could be fetched; baseline left unchanged.")
        for err in errors:
            print("FETCH_ERROR", err)
        set_output("meaningful_changes", 0)
        set_output("fetch_errors", len(errors))
        return 2

    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    baseline_payload = {"version": 1, "snapshots": next_baseline}
    baseline_path.write_text(json.dumps(baseline_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = []
    if seeded:
        lines += [
            "# Competitor Watch Baseline",
            "",
            f"Baseline seeded for **{successes}** priority competitor pages. No change alert is issued on the first snapshot.",
            "",
            "Future runs compare title/H1/meta, canonical/robots, schema types, important internal links, conversion/local signals and aggressive guarantee language.",
        ]
    elif not alerts:
        lines += [
            "# Competitor Watch",
            "",
            f"No meaningful competitor changes detected across **{successes}** successfully fetched priority pages.",
            "",
            "Decision: **PROTECT** current owner pages. Do not rewrite solely because the watcher ran.",
        ]
    else:
        lines += [
            "# Competitor SEO Change Report",
            "",
            f"Meaningful competitor changes detected: **{len(alerts)}**.",
            "",
        ]
        for item in alerts:
            t = item["target"]
            cur = item["current"]
            ours = item["ours"] or {}
            lines += [
                f"## {t['competitor']} — {t['market']}",
                "",
                f"**Target query + market:** free appliance pickup {t['market']}; appliance pickup {t['market']}",
                "",
                f"**Observed competitor move:** {describe_changes(item['changes'])}",
                "",
                "**Competitor strength:** " + (", ".join(strengths(cur.get("signals", {}))) or "no benchmark signal detected") + ".",
                "",
                "**Our current strength:** " + (", ".join(strengths(ours.get("signals", {}))) or "owner page unavailable or no benchmark signals detected") + ".",
                "",
                "**Our gap:** " + (", ".join(item["gaps"]) if item["gaps"] else "No material benchmark gap detected from this change.") ,
                "",
                "**Exact countermove:** " + " ".join(item["countermoves"]),
                "",
                "**Risk check:** Preserve the existing intent owner. Do not create a duplicate city page, thin city×appliance page, false local-presence claim, or blanket free/same-day guarantee.",
                "",
                "**Recheck plan:** Run repository audits, submit only changed owner URLs through the existing IndexNow workflow, then use the exact live search and later Search Console evidence before another rewrite.",
                "",
            ]

    if errors:
        lines += ["## Fetch notes", ""]
        lines += [f"- {err}" for err in errors]
        lines += ["", "Failed targets keep their previous baseline and do not create false change alerts."]

    report_text = "\n".join(lines).rstrip() + "\n"
    report_path.write_text(report_text, encoding="utf-8")

    print(f"TARGETS={len(config.get('targets', []))}")
    print(f"FETCHED={successes}")
    print(f"FETCH_ERRORS={len(errors)}")
    print(f"MEANINGFUL_CHANGES={len(alerts)}")
    print(f"SEEDED={str(seeded).lower()}")
    for item in alerts:
        print("CHANGE", item["target"]["id"], "::", describe_changes(item["changes"]))
        for move in item["countermoves"]:
            print("COUNTERMOVE", item["target"]["id"], "::", move)
    for err in errors:
        print("FETCH_ERROR", err)

    set_output("meaningful_changes", len(alerts))
    set_output("fetch_errors", len(errors))
    set_output("seeded", str(seeded).lower())
    return 0

if __name__ == "__main__":
    sys.exit(main())
