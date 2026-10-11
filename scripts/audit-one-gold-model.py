#!/usr/bin/env python3
"""Read-only rollout QA for the One Gold Model. No city pages are generated."""
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://freereliableappliancepickup.com"

def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def slugify(city):
    value = unicodedata.normalize("NFKD", city.lower())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", value))

def html_attrs(tag):
    return dict((k.lower(), v) for k, v in re.findall(r'([\w:-]+)\s*=\s*["\x27]([^"\x27]*)["\x27]', tag))

def inspect_city_page(slug, state_code, experiments, today):
    path = ROOT / (slug + "-appliance-pickup") / "index.html"
    route = "/" + slug + "-appliance-pickup/"
    if not path.is_file():
        return {"citySlug": slug, "url": route, "exists": False, "status": "regional-request-review-only"}
    html = path.read_text(encoding="utf-8")
    head = html.split("</head>", 1)[0]
    tags = re.findall(r"<link\b[^>]*>", head, flags=re.IGNORECASE)
    canonicals = [html_attrs(tag).get("href") for tag in tags if html_attrs(tag).get("rel", "").lower() == "canonical"]
    h1_count = len(re.findall(r"<h1\b", html, flags=re.IGNORECASE))
    forms = re.findall(r"<form\b[\s\S]*?</form>", html, flags=re.IGNORECASE)
    request_forms = [f for f in forms if "formspree.io/" in f.lower()]
    input_names = set(re.findall(r'<(?:input|select|textarea)\b[^>]*\bname=["\x27]([^"\x27]+)', "".join(request_forms), flags=re.IGNORECASE))
    links = re.findall(r'<a\b[^>]*\bhref=["\x27]([^"\x27]+)', html, flags=re.IGNORECASE)
    own_phone_link = any(link.startswith("tel:") for link in links)
    broken = []
    for link in links:
        if not link or link.startswith(("#", "mailto:", "sms:", "tel:", "javascript:")):
            continue
        absolute = urljoin(DOMAIN + route, link)
        url = urlparse(absolute)
        if url.netloc not in ("freereliableappliancepickup.com", "www.freereliableappliancepickup.com"):
            continue
        file_path = url.path.lstrip("/")
        if not file_path:
            file_path = "index.html"
        elif file_path.endswith("/"):
            file_path += "index.html"
        if not (ROOT / file_path).exists() and file_path not in broken:
            broken.append(file_path)
    guarded = [
        {"experiment": e.get("id"), "reviewNotBefore": e.get("evaluateNotBefore")}
        for e in experiments
        if e.get("status") == "running"
        and (e.get("evaluateNotBefore") or "0000-01-01") > today
        and route in (
            list(e.get("pagesChanged") or [])
            + ([e["protectedOwner"]] if e.get("protectedOwner") else [])
            + list(e.get("protectedOwners") or [])
        )
    ]
    return {
        "citySlug": slug, "url": route, "exists": True, "stateCode": state_code,
        "titlePresent": bool(re.search(r"<title>\s*[^<]+\s*</title>", head, flags=re.IGNORECASE)),
        "canonicalMatches": canonicals == [DOMAIN + route],
        "h1Count": h1_count,
        "hasRequestForm": bool(request_forms),
        "formHasCityStateCondition": {"city", "state", "condition"}.issubset(input_names),
        "formHasSourcePage": "source_page" in input_names,
        "hasTapToCall": own_phone_link,
        "localBrokenLinks": sorted(broken),
        "protectedExperiment": guarded,
        "editRule": "wait for evaluation or separately log a verified technical fix" if guarded else "use evidence-led targeted changes",
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="reports/one-gold-model-audit.json")
    args = ap.parse_args()
    config = read_json("data/one-gold-model-rollout.json")
    routing = read_json("data/market-routing.json")
    cities = read_json("data/cities.json")["cities"]
    experiments = read_json("data/seo-experiments.json").get("experiments", [])
    today = date.today().isoformat()
    phases = []
    scanned = []
    for phase in config["rollout"]:
        code = phase.get("stateCode")
        if code:
            selected = [c for c in cities if c.get("state_code") == code]
            all_pages = [inspect_city_page(slugify(c["city"]), code, experiments, today) for c in selected]
            existing = sum(p["exists"] for p in all_pages)
            metro = {}
            for c, page in zip(selected, all_pages):
                bucket = metro.setdefault(c.get("region") or "Other", {"registeredCities": [], "existingCityPages": [], "intakeOnly": []})
                bucket["registeredCities"].append(c["city"])
                bucket["existingCityPages" if page["exists"] else "intakeOnly"].append(c["city"])
            phases.append({
                "id": phase["id"], "state": code, "registeredCities": len(selected), "existingGeneralCityPages": existing,
                "missingCityPagesAreNotAutomaticWork": True,
                "regionalCoverageRegistry": metro,
                "priorityPageAudits": [inspect_city_page(slug, code, experiments, today) for slug in phase["priorityGeneralPages"]],
            })
            scanned.extend(all_pages)
        else:
            phases.append({"id": phase["id"], "priorityRegions": phase.get("priorityRegions", []),
                           "rule": "Verify direct or approved-partner capacity before any indexable city expansion."})
    active_direct = [
        {"state": x.get("state_code"), "region": x.get("region"), "city": x.get("city")}
        for x in routing.get("markets", []) if x.get("status") == "direct"
    ]
    issues = {
        "missingFormSource": [p["url"] for p in scanned if p["exists"] and p.get("hasRequestForm") and not p.get("formHasSourcePage")],
        "canonicalMismatch": [p["url"] for p in scanned if p["exists"] and not p.get("canonicalMatches")],
        "multipleOrMissingH1": [p["url"] for p in scanned if p["exists"] and p.get("h1Count") != 1],
        "brokenInternalReferences": [{"url": p["url"], "paths": p["localBrokenLinks"]} for p in scanned if p["exists"] and p.get("localBrokenLinks")],
    }
    report = {
        "name": config["name"], "asOf": today, "source": "GitHub repository audit only, not a live URL or Google rank check",
        "activeProtectedExperiments": sum(e.get("status") == "running" for e in experiments),
        "confirmedDirectMarketRecords": active_direct,
        "phases": phases, "improvementQueue": issues,
        "approvalGate": "No automatic city-page generation, changes to frozen ranking experiments, new GBP locations, or unverified service promises.",
    }
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for phase in phases:
        if "state" in phase:
            print(f"{phase['id']}: {phase['existingGeneralCityPages']} existing city pages / {phase['registeredCities']} registry cities")
            for name, bucket in phase["regionalCoverageRegistry"].items():
                print(f"  {name}: {len(bucket['existingCityPages'])} existing, {len(bucket['intakeOnly'])} regional-intake-only")
    print("Protected experiments:", report["activeProtectedExperiments"])
    for key, value in issues.items():
        print(f"Review {key}: {len(value)}")
    print("Report:", out.relative_to(ROOT))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
