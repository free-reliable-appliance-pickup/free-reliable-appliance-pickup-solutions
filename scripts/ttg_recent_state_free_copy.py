#!/usr/bin/env python3
"""Customer-facing California-model wording for Nov 9-10 TTG states.
Preserve all live form fields, images, disclosures and existing index directives.
Use: python3 scripts/ttg_recent_state_free_copy.py --apply|--check
"""
from html import escape, unescape
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
STATES = {
    "IL": "Illinois", "IN": "Indiana", "MI": "Michigan",
    "MN": "Minnesota", "NC": "North Carolina", "OH": "Ohio",
    "PA": "Pennsylvania", "TN": "Tennessee", "VA": "Virginia",
    "WI": "Wisconsin",
}
KINDS = {
    "washer-dryer": "Washer & Dryer", "refrigerator": "Refrigerator",
    "stove-oven": "Stove & Oven", "freezer": "Freezer", "appliance": "Appliance",
}
FORM = "https://formspree.io/f/mvzeapzd"
CORE = (
    "name", "phone", "address", "city", "state", "zip",
    "appliance", "condition", "floor", "stairs",
    "photos_available", "access", "message", "privacy_acknowledgment",
)

def targets():
    result = {}
    for code, state in STATES.items():
        manifest = ROOT / "data" / "ttg-state-batches" / (code + ".json")
        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data.get("state_code") == code and data.get("mode") == "request-only"
        paths = list(data["pages"]) + [
            state.lower().replace(" ", "-") + "-appliance-pickup/index.html"
        ]
        for rel in paths:
            path = ROOT / rel
            if not path.is_file() or not path.resolve().is_relative_to(ROOT):
                raise RuntimeError("Missing / unsafe request page: " + rel)
            result[rel] = code
    return result

def kind_and_city(rel, code):
    slug = Path(rel).parent.name
    for key in KINDS:
        suffix = "-" + code.lower() + "-" + key + "-pickup"
        if slug.endswith(suffix):
            return key, slug[:-len(suffix)]
    if slug == STATES[code].lower().replace(" ", "-") + "-appliance-pickup":
        return "appliance", None
    raise RuntimeError("Unknown kind: " + rel)

def city_name(slug, code, original):
    if slug is None:
        return STATES[code]
    title = re.search(r"<title>(.*?)</title>", original, re.I | re.S)
    current = unescape(title.group(1)) if title else ""
    match = re.search(r"^(.+?),\s*" + code + r"\b", current)
    if match:
        return match.group(1).strip()
    return " ".join(x.capitalize() for x in slug.split("-"))

def clean_copy(raw):
    s = raw
    replacements = [
        (r"\bfree appliance pickup eligibility requests?\b", "free appliance pickup requests"),
        (r"\bfree appliance pickup eligibility\b", "free appliance pickup"),
        (r"\bfree pickup eligibility\b", "free pickup availability"),
        (r"\bappliance pickup eligibility\b", "appliance pickup requests"),
        (r"\bpickup eligibility\b", "pickup review"),
        (r"\beligibility review\b", "pickup request review"),
        (r"\beligibility requests?\b", "pickup requests"),
        (r"\beligibility inquiries\b", "pickup requests"),
        (r"\beligibility guides?\b", "pickup guides"),
        (r"\beligibility markets\b", "pickup locations"),
        (r"\beligibility\b", "pickup details"),
    ]
    for pat, repl in replacements:
        s = re.sub(pat, repl, s, flags=re.I)
    return s

def visible_nodes(s):
    # Never change scripts/styles or HTML attributes; retain form field keys and hrefs.
    sections = re.split(
        r"(<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>)",
        s, flags=re.I,
    )
    for i in range(0, len(sections), 2):
        sections[i] = re.sub(
            r"(?<=>)[^<>]+(?=<)",
            lambda m: clean_copy(m.group(0)),
            sections[i],
        )
    return "".join(sections)

def revise(original, rel, code):
    kind, slug = kind_and_city(rel, code)
    city = city_name(slug, code, original)
    label = KINDS[kind]
    loc = city if slug is None else city + ", " + code
    heading = "Free " + label + " Pickup in " + loc
    title = heading + " | Free Reliable Appliance Pickup"
    s = original
    if rel == "north-carolina-appliance-pickup/index.html":
        # Statewide NC template predates the required California intake contract.
        old = '<input type="hidden" name="state" value="North Carolina">'
        new = '<div class="site-request-field"><label>Pickup state<select name="state" required><option value="North Carolina" selected>North Carolina</option></select></label></div>'
        if s.count(old) != 1:
            raise RuntimeError("NC statewide state field changed unexpectedly")
        s = s.replace(old, new)
        s = s.replace('name="access" placeholder=', 'name="access" required placeholder=')
        s = s.replace('name="message" rows=', 'name="message" required rows=')
        photo_marker = '<div class="site-request-field full"><label>Access Details'
        photo_field = '<div class="site-request-field"><label>Photos available?<select name="photos_available" required><option value="">Choose one</option><option>Yes, I can share appliance photos</option><option>No photos yet</option><option>Need help sharing photos</option></select></label></div>'
        if s.count(photo_marker) != 1:
            raise RuntimeError("NC access field changed unexpectedly")
        s = s.replace(photo_marker, photo_field + photo_marker)
        button_marker = '<div class="site-request-field full"><button class="site-request-submit"'
        privacy_field = '<div class="site-request-field full"><p class="site-request-note">Privacy: We use your contact, appliance condition and removal details to review this request through Formspree and may share them with a prospective pickup operator. Read our <a href="/privacy/">Privacy Policy</a>.</p><label style="display:flex;align-items:flex-start;gap:10px"><input type="checkbox" name="privacy_acknowledgment" value="acknowledged" required style="width:22px;min-width:22px;height:22px;margin:4px 0 0">I understand this is a request for free appliance pickup, not a confirmed appointment.</label></div>'
        if s.count(button_marker) != 1:
            raise RuntimeError("NC submit field changed unexpectedly")
        s = s.replace(button_marker, privacy_field + button_marker)
    title_match = re.search(r"<title>[^<]*</title>", s, re.I)
    if not title_match:
        raise RuntimeError("Missing title: " + rel)
    s = s[:title_match.start()] + "<title>" + escape(title) + "</title>" + s[title_match.end():]
    h1 = list(re.finditer(r"<h1\b[^>]*>[\s\S]*?</h1>", s, re.I))
    if len(h1) != 1:
        raise RuntimeError("Wrong number of headings: " + rel)
    s = s[:h1[0].start()] + "<h1>" + escape(heading) + "</h1>" + s[h1[0].end():]

    def heading2(m):
        text = unescape(re.sub("<[^>]+>", "", m.group(2)))
        low = text.lower()
        if "eligibilit" in low or "market research" in low or "competitor" in low or "demand regions" in low:
            if "how " in low or low.startswith("how"):
                replacement = "How Free " + label + " Pickup Works in " + city
            elif "request" in low or "submit" in low or "send" in low:
                replacement = "Request Free " + label + " Pickup in " + loc
            elif "city" in low or "cities" in low or "markets" in low or "regions" in low or "guide" in low:
                replacement = "Free Appliance Pickup Locations in " + STATES[code]
            else:
                replacement = "Free " + label + " Pickup Details in " + city
            return m.group(1) + escape(replacement) + m.group(3)
        return m.group(0)
    s = re.sub(r"(<h2\b[^>]*>)([\s\S]*?)(</h2>)", heading2, s, flags=re.I)
    s = visible_nodes(s)

    # Actual submission button on each pre-existing request form.
    def button(match):
        t = unescape(re.sub(r"<[^>]+>", "", match.group(2))).strip().lower()
        if any(word in t for word in ("submit", "request", "eligibility")):
            return match.group(1) + "Request Free " + escape(label) + " Pickup" + match.group(3)
        return match.group(0)
    s = re.sub(r"(<button\b[^>]*>)([^<]*)(</button>)", button, s, flags=re.I)

    # Keep linked destinations, but use customer-facing labels rather than eligibility.
    def anchor(match):
        prefix, dest_slug, dest_kind, text, end = match.groups()
        if not any(x in unescape(text).lower() for x in ("eligib", "pickup", "request", "guide")):
            return match.group(0)
        dst = dest_slug.rsplit("-" + code.lower() + "-", 1)[0]
        dest_city = " ".join(w.capitalize() for w in dst.split("-"))
        # Use current page city where appropriate; no new coverage assertions.
        if slug and dst == slug:
            dest_city = city
        new_label = dest_city + " Free " + KINDS[dest_kind] + " Pickup"
        return prefix + escape(new_label) + end
    kind_re = r"(washer-dryer|refrigerator|stove-oven|freezer|appliance)"
    s = re.sub(
        r'(<a\b[^>]*href="/([a-z0-9-]+-' + code.lower() + r'-' +
        kind_re + r'-pickup)/"[^>]*>)([^<]+)(</a>)',
        anchor, s, flags=re.I,
    )

    # Preserve current local description detail, change only customer-facing wording.
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', s, re.I)
    description = clean_copy(unescape(desc_match.group(1))) if desc_match else (
        "Request free " + label.lower() + " pickup in " + loc +
        " with Free Reliable Appliance Pickup. Availability must be confirmed."
    )
    if desc_match:
        s = (s[:desc_match.start(1)] + escape(description, quote=True)
             + s[desc_match.end(1):])
    for prop, value in (("og:title", title), ("og:description", description), ("twitter:title", title), ("twitter:description", description)):
        s = re.sub(
            r'(<meta\b[^>]*property="' + prop + r'"[^>]*content=")[^"]*(")',
            lambda m: m.group(1) + escape(value, quote=True) + m.group(2),
            s, flags=re.I,
        )
    # Some state hubs use the name/content ordering rather than property.
    def ldjson(match):
        try:
            data = json.loads(match.group(2))
        except json.JSONDecodeError:
            return match.group(0)
        def walk(node):
            if isinstance(node, list):
                for item in node: walk(item)
            elif isinstance(node, dict):
                tp = node.get("@type", [])
                if tp == "WebPage" or isinstance(tp, list) and "WebPage" in tp:
                    node["name"] = title
                    if "description" in node:
                        node["description"] = description
                for key, val in list(node.items()):
                    if isinstance(val, (dict, list)):
                        walk(val)
                    elif isinstance(val, str) and key in {"name", "description", "text", "headline"} and "eligibilit" in val.lower():
                        node[key] = clean_copy(val)
        walk(data)
        return match.group(1) + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + match.group(3)
    s = re.sub(
        r'(<script\b[^>]*type="application/ld\+json"[^>]*>)([\s\S]*?)(</script>)',
        ldjson, s, flags=re.I,
    )
    return s

def checks(before, after, rel, code):
    kind, slug = kind_and_city(rel, code)
    wanted = "Free " + KINDS[kind] + " Pickup"
    errors = []
    def err(condition, issue):
        if condition: errors.append(issue)
    heading = re.search(r"<h1[^>]*>(.*?)</h1>", after, re.I | re.S)
    title = re.search(r"<title>(.*?)</title>", after, re.I | re.S)
    err(not heading or wanted not in unescape(heading.group(1)), "incorrect H1")
    err(not title or wanted not in unescape(title.group(1)), "incorrect title")
    err("Free Reliable Appliance Pickup" not in unescape(title.group(1) if title else ""), "missing branded title")
    err("Free Reliable Appliance Pickup" not in after, "missing business brand")
    err(FORM not in after, "missing authorized Formspree endpoint")
    err('name="source_page"' not in after, "missing source_page attribution")
    err(len(re.findall(r"<form\b", before, re.I)) != len(re.findall(r"<form\b", after, re.I)), "form count changed")
    err(len(re.findall(r"<img\b", before, re.I)) != len(re.findall(r"<img\b", after, re.I)), "image count changed")
    err(len(re.findall(r'<meta name="robots"[^>]*>', before, re.I)) != len(re.findall(r'<meta name="robots"[^>]*>', after, re.I)), "robots meta changed")
    old_robots = re.findall(r'<meta name="robots"[^>]*>', before, re.I)
    new_robots = re.findall(r'<meta name="robots"[^>]*>', after, re.I)
    err(old_robots != new_robots, "robot directives modified")
    err(len(re.findall(r"<h1\b", after, re.I)) != 1, "not exactly one H1")
    for field in CORE:
        pat = r'<(?:input|select|textarea)\b[^>]*name="' + field + r'"[^>]*required'
        err(not re.search(pat, after, re.I), "missing mandatory field " + field)
    content_no_code = re.sub(r'<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>', "", after, flags=re.I)
    human_text = " ".join(re.findall(r">([^<>]+)<", content_no_code))
    err("eligibilit" in unescape(human_text).lower(), "eligibility wording remains visible")
    err("eligibilit" in unescape(after[after.index("<title>"):after.index("</title>")]).lower(), "eligibility in title")
    for tag in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>([\s\S]*?)</script>', after, re.I):
        try: json.loads(tag)
        except json.JSONDecodeError: errors.append("invalid JSON-LD")
    return errors

def run(mode):
    items = targets()
    reports = []
    staged = []
    for rel, code in sorted(items.items()):
        path = ROOT / rel
        before = path.read_text(encoding="utf-8")
        after = revise(before, rel, code) if mode == "--apply" else before
        problems = checks(before, after, rel, code)
        if problems:
            reports.append(rel + ": " + "; ".join(problems))
        elif before != after:
            staged.append((path, after))
    if reports:
        print("FAILED pages:", len(reports))
        print("\n".join(reports[:100]))
        sys.exit(1)
    for path, data in staged:
        path.write_text(data, encoding="utf-8")
    print("PASS: validated", len(items), "recent state request pages; corrected", len(staged), "pages", "(mode:", mode + ")")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("--apply", "--check"):
        sys.exit("Usage: ttg_recent_state_free_copy.py --apply|--check")
    run(sys.argv[1])
