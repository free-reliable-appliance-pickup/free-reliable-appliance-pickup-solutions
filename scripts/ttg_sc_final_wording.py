#!/usr/bin/env python3
"""Final customer-facing SC wording pass; preserve photos, forms and noindex."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"appliance": "Appliance", "washer-dryer": "Washer &amp; Dryer",
         "refrigerator": "Refrigerator", "stove-oven": "Stove &amp; Oven",
         "freezer": "Freezer"}
MANIFEST = ROOT / "data/ttg-state-batches/SC.json"

def revise(content, rel):
    slug = Path(rel).parent.name
    matches = [key for key in KINDS if slug.endswith("-sc-" + key + "-pickup")]
    kind = matches[0] if matches else "appliance"
    item = KINDS[kind]
    title = re.search(r"<title>([^<]+), SC Free", content)
    city = title.group(1) if title else "South Carolina"
    s = content

    def link_label(match):
        prefix, label, suffix = match.groups()
        label = re.sub(
            r"\b(Appliance|Washer &amp; Dryer|Refrigerator|Stove &amp; Oven|Freezer)$",
            lambda m: "Free " + m.group(1) + " Pickup", label, flags=re.I)
        return prefix + label + suffix

    s = re.sub(r"(<a\b[^>]*>)([^<]*?) eligibility(</a>)",
               link_label, s, flags=re.I)
    s = re.sub(r"(<h[1-6][^>]*>)[^<]* used-appliance eligibility(</h[1-6]>)",
               lambda m: m.group(1) + "Free " + item +
               " Pickup Details in " + city + m.group(2), s, flags=re.I)
    s = re.sub(r"(<h[1-6][^>]*>)Reviewing ([^<]+) in ([^<]+)(</h[1-6]>)",
               lambda m: m.group(1) + "Free " + m.group(2).title() +
               " Pickup Details in " + m.group(3) + m.group(4), s, flags=re.I)
    s = re.sub(r"How this eligibility request works|How the conditional request works",
               "How to Request Free " + item + " Pickup", s, flags=re.I)
    s = re.sub(r"for eligibility review", "to review your pickup request", s, flags=re.I)
    s = re.sub(r"These 50 city guides provide eligibility review only\.",
               "These 50 city pages accept free appliance pickup requests. Pickup must be confirmed before scheduling.", s, flags=re.I)
    s = re.sub(r"eligibility review only", "free appliance pickup requests only", s, flags=re.I)
    s = re.sub(r"(<button\b[^>]*>)Submit [^<]*? request(</button>)",
               lambda m: m.group(1) + "Request Free " + item + " Pickup" + m.group(2), s, flags=re.I)
    s = re.sub(r"(<h[1-6][^>]*>)Send [^<]*? request(</h[1-6]>)",
               lambda m: m.group(1) + "Request Free " + item + " Pickup in " + city + m.group(2), s, flags=re.I)
    s = re.sub(r"Request-only:", "Service confirmation:", s, flags=re.I)
    s = s.replace("Free Washer &amp; dryer Pickup", "Free Washer &amp; Dryer Pickup")
    s = s.replace("Free Stove &amp; oven Pickup", "Free Stove &amp; Oven Pickup")
    if "eligibilit" in s.lower():
        raise RuntimeError(f"Unreplaced eligibility label: {rel}")
    if "Free Reliable Appliance Pickup" not in s or "<h1>" not in s or "<form" not in s:
        raise RuntimeError(f"Required brand, headline or form absent: {rel}")
    if 'content="noindex, follow"' not in s:
        raise RuntimeError(f"Unconfirmed coverage must remain noindex: {rel}")
    return s

data = json.loads(MANIFEST.read_text(encoding="utf-8"))
pages = data["pages"]
if data.get("state_code") != "SC" or len(pages) != 251 or len(set(pages)) != 251:
    raise RuntimeError("Expected exactly 251 unique South Carolina page paths")
changes = []
for rel in pages:
    path = (ROOT / rel).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise RuntimeError(f"Missing or unsafe page: {rel}")
    before = path.read_text(encoding="utf-8")
    after = revise(before, rel)
    if before != after:
        changes.append((path, after))
for path, content in changes:
    path.write_text(content, encoding="utf-8")
print(f"South Carolina California model: corrected {len(changes)} of {len(pages)} pages")
