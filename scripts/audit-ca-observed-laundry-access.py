#!/usr/bin/env python3
"""Offline, no-submit intake regression guard for six observed California laundry pages."""
from html.parser import HTMLParser
from pathlib import Path
import sys

CITIES = {
    "sacramento-metro": ("", "required_blank", "Washer Dryer Pickup"),
    "visalia": ("Visalia", "hidden", "Washer and dryer pickup"),
    "san-francisco": ("San Francisco", "hidden", "Washer and dryer pickup"),
    "san-luis-obispo": ("San Luis Obispo", "hidden", "Washer and dryer pickup"),
    "hesperia": ("Hesperia", "visible_fixed", "Washer and dryer pickup"),
    "san-marcos": ("San Marcos", "hidden", "Washer and dryer pickup"),
}
ENDPOINT = "https://formspree.io/f/mvzeapzd"


class FormReader(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms = []
        self.current = None
        self.select = None
        self.option = None
        self.ancestors = []

    def _disabled_by_fieldset(self):
        """Disabled fieldsets exempt controls inside their first direct legend."""
        for ancestor in self.ancestors:
            if ancestor["tag"] != "fieldset" or "disabled" not in ancestor["attrs"]:
                continue
            first_legend = ancestor.get("first_legend")
            if first_legend is None or not any(
                node is first_legend for node in self.ancestors
            ):
                return True
        return False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form":
            self.current = {"attrs": attrs, "fields": []}
            self.forms.append(self.current)
            self.ancestors = []
        elif self.current is not None:
            node = {"tag": tag, "attrs": attrs}
            parent = self.ancestors[-1] if self.ancestors else None
            if tag == "legend" and parent and parent["tag"] == "fieldset":
                if "first_legend" not in parent:
                    parent["first_legend"] = node
            effectively_disabled = (
                "disabled" in attrs or self._disabled_by_fieldset()
            )
            if tag in ("input", "select", "textarea"):
                field = {"tag": tag, "attrs": attrs, "options": [],
                         "effectively_disabled": effectively_disabled}
                self.current["fields"].append(field)
                if tag == "select":
                    self.select = field
            elif tag == "option" and self.select is not None:
                disabled_group = any(
                    ancestor["tag"] == "optgroup"
                    and "disabled" in ancestor["attrs"]
                    for ancestor in self.ancestors
                )
                self.option = {"attrs": attrs, "text": "",
                               "effectively_disabled": effectively_disabled or disabled_group}
                self.select["options"].append(self.option)
            if tag not in self.VOID:
                self.ancestors.append(node)

    def handle_data(self, data):
        if self.option is not None:
            self.option["text"] += data

    def handle_endtag(self, tag):
        if tag == "option":
            self.option = None
        elif tag == "select":
            self.select = None
        elif tag == "form":
            self.current = None
            self.ancestors = []
            return
        for i in range(len(self.ancestors) - 1, -1, -1):
            if self.ancestors[i]["tag"] == tag:
                del self.ancestors[i:]
                break


def check(html, slug, city, city_mode, service):
    parser = FormReader()
    parser.feed(html)
    faults = []
    if len(parser.forms) != 1:
        return [f"{slug}: exactly one pickup form required, got {len(parser.forms)}"]
    form = parser.forms[0]
    if form["attrs"].get("action") != ENDPOINT or form["attrs"].get("method", "").lower() != "post":
        faults.append(f"{slug}: form must POST to exact known Formspree endpoint")
    fields = form["fields"]

    def named(field):
        return [x for x in fields if x["attrs"].get("name") == field]

    def one(field, tag=None):
        matches = named(field)
        if len(matches) != 1 or (tag is not None and matches[0]["tag"] != tag):
            faults.append(f"{slug}: expected exactly one native {tag or 'field'} named {field}")
            return None
        return matches[0]

    for field, value in (
        ("source_page", slug + "-washer-dryer-pickup"),
        ("state", "California"),
        ("service", service),
    ):
        element = one(field, "input")
        if element and (element["attrs"].get("type") != "hidden" or element["attrs"].get("value") != value):
            faults.append(f"{slug}: incorrect static {field} attribution")
    customer_city = one("city", "input")
    if customer_city:
        a = customer_city["attrs"]
        if city_mode == "hidden":
            if a.get("type") != "hidden" or a.get("value") != city:
                faults.append(f"{slug}: incorrect hidden city")
        elif city_mode == "visible_fixed":
            if a.get("type") == "hidden" or "required" not in a or a.get("value") != city:
                faults.append(f"{slug}: incorrect required visible city")
        elif city_mode == "required_blank":
            if a.get("type") == "hidden" or "required" not in a or a.get("value") not in (None, ""):
                faults.append(f"{slug}: metro request must ask customer for city")

    for field in ("name", "phone", "address", "zip"):
        el = one(field, "input")
        if el and "required" not in el["attrs"]:
            faults.append(f"{slug}: {field} must use native required")
        if field == "phone" and el and el["attrs"].get("type") != "tel":
            faults.append(f"{slug}: phone must have mobile telephone type")

    for field in ("appliance", "condition", "location", "stairs"):
        el = one(field, "select")
        if not el:
            continue
        if "required" not in el["attrs"]:
            faults.append(f"{slug}: {field} select missing required")
        if el["effectively_disabled"]:
            faults.append(f"{slug}: {field} select cannot be disabled")
        options = el["options"]
        if not options or options[0]["attrs"].get("value") != "":
            faults.append(f"{slug}: {field} must start with an empty-value prompt")
        if any("selected" in o["attrs"] for o in options[1:]):
            faults.append(f"{slug}: {field} has nonempty preselected default")
        if field in ("location", "stairs") and not any(
            ("unknown" in o["text"].lower() or "not sure" in o["text"].lower())
            and not o["effectively_disabled"]
            and (o["attrs"].get("value", o["text"].strip()) != "")
            for o in options[1:]
        ):
            faults.append(f"{slug}: {field} needs an enabled nonblank unknown option after the prompt")
    return faults


def fixture(slug, city, mode, service):
    city_html = (
        f'<input type="hidden" name="city" value="{city}">'
        if mode == "hidden" else (
            f'<input name="city" value="{city}" required>'
            if mode == "visible_fixed" else '<input type="text" name="city" required>'
        )
    )
    html = (f'<form action="{ENDPOINT}" method="POST">'
            f'<input type="hidden" name="source_page" value="{slug}-washer-dryer-pickup">'
            '<input type="hidden" name="state" value="California">'
            f'<input type="hidden" name="service" value="{service}">'
            + city_html)
    for name in ("name", "phone", "address", "zip"):
        html += f'<input name="{name}" type="{"tel" if name == "phone" else "text"}" required>'
    for name in ("appliance", "condition", "location", "stairs"):
        html += f'<select name="{name}" required><option value="">Select</option><option>Unknown / not sure</option></select>'
    return html + "</form>"


def self_test():
    for slug in ("visalia", "hesperia", "sacramento-metro"):
        city, mode, service = CITIES[slug]
        valid = fixture(slug, city, mode, service)
        assert not check(valid, slug, city, mode, service), f"{slug}: positive test failed"
    city, mode, service = CITIES["visalia"]
    valid = fixture("visalia", city, mode, service)
    broken = [
        valid.replace('name="location"', 'data-name="location"'),
        valid.replace('name="stairs" required', 'name="stairs" data-required="true"'),
        valid.replace(ENDPOINT, ENDPOINT + "-typo"),
        valid.replace('<select name="location" required><option value="">Select</option><option>Unknown / not sure</option></select>',
                      '<input name="location" required>'),
        valid.replace('<option>Unknown / not sure</option>', '<option selected>Unknown / not sure</option>', 1),
        valid.replace('<select name="stairs" required><option value="">',
                      '<select name="stairs" required><option value="None">'),
        valid.replace('name="source_page"', 'name="source_missing"'),
        valid.replace('name="city" value="Visalia"', 'name="city" value="Wrong City"'),
        valid.replace('name="service" value="Washer and dryer pickup"',
                      'name="service" value="General pickup"'),
        valid.replace('name="location" required', 'name="location" required disabled'),
        valid.replace('<select name="location" required><option value="">Select</option><option>Unknown / not sure</option></select>',
                      '<select name="location" required><option value="">Unknown / not sure</option></select>'),
        valid.replace('<select name="location" required><option value="">Select</option><option>Unknown / not sure</option></select>',
                      '<select name="location" required><option value="">Select</option><option disabled>Unknown / not sure</option></select>'),
        # A disabled ancestor fieldset makes a required select unusable.
        valid.replace('<select name="location" required>',
                      '<fieldset disabled><select name="location" required>')
             .replace('</select><select name="stairs" required>',
                      '</select></fieldset><select name="stairs" required>'),
        # A disabled fieldset's second legend is NOT exempt.
        valid.replace('<select name="location" required>',
                      '<fieldset disabled><legend>First</legend><legend><select name="location" required>')
             .replace('</select><select name="stairs" required>',
                      '</select></legend></fieldset><select name="stairs" required>'),
        # A first legend does not exempt a select placed after it.
        valid.replace('<select name="location" required>',
                      '<fieldset disabled><legend>Location</legend><select name="location" required>')
             .replace('</select><select name="stairs" required>',
                      '</select></fieldset><select name="stairs" required>'),
        # An Unknown answer inside a disabled optgroup cannot be chosen.
        valid.replace('<option>Unknown / not sure</option></select><select name="stairs"',
                      '<optgroup disabled label="Other"><option>Unknown / not sure</option></optgroup></select><select name="stairs"'),
    ]
    for i, altered in enumerate(broken, 1):
        assert check(altered, "visalia", city, mode, service), f"negative fixture {i} escaped"
    # Controls within a disabled fieldset's FIRST direct legend remain enabled.
    legend_form = valid.replace('<select name="location" required>',
                                '<fieldset disabled><legend><select name="location" required>')
    legend_form = legend_form.replace('</select><select name="stairs" required>',
                                      '</select></legend></fieldset><select name="stairs" required>')
    assert not check(legend_form, "visalia", city, mode, service), (
        "first-legend exception incorrectly rejected"
    )
    metro, m, s = CITIES["sacramento-metro"]
    metro_form = fixture("sacramento-metro", metro, m, s)
    assert check(metro_form.replace('name="city" required',
                                    'name="city" value="Sacramento" required'),
                 "sacramento-metro", metro, m, s), "fixed metro city escaped"
    print("PASS: four positive and seventeen negative offline intake fixtures")


def main():
    self_test()
    issues = []
    for slug, (city, mode, service) in CITIES.items():
        page = Path(f"{slug}-washer-dryer-pickup/index.html")
        if not page.is_file():
            issues.append(f"{slug}: existing page missing")
            continue
        issues.extend(check(page.read_text(encoding="utf-8"), slug, city, mode, service))
    if issues:
        print("\n".join(issues))
        sys.exit(1)
    print(f"PASS: {len(CITIES)} observed California laundry forms have native blank-first access selects and reliable attribution")


if __name__ == "__main__":
    main()
