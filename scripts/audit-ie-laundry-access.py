#!/usr/bin/env python3
"""Offline regression guard for eight existing Inland Empire laundry pickup forms.

Does not transmit customer data, test live Formspree delivery, or assert service availability.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

CITIES = {
    "eastvale": "Eastvale",
    "jurupa-valley": "Jurupa Valley",
    "moreno-valley": "Moreno Valley",
    "menifee": "Menifee",
    "perris": "Perris",
    "murrieta": "Murrieta",
    "banning": "Banning",
    "beaumont": "Beaumont",
}
FORM_RE = re.compile(r"<form\b[^>]*>[\s\S]*?</form>", re.I)
SELECT_RE = re.compile(r"<select\b([^>]*)>([\s\S]*?)</select>", re.I)
INPUT_RE = re.compile(r"<input\b[^>]*>", re.I)
OPTION_RE = re.compile(r"<option\b[^>]*>", re.I)


class OptionAttributes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.options = []

    def handle_starttag(self, tag, attrs):
        if tag == "option":
            self.options.append(dict(attrs))


def attribute(tag, name):
    match = re.search(r'(?<![\w:-])' + re.escape(name) + r'\s*=\s*["\x27]([^"\x27]*)["\x27]', tag, re.I)
    return match.group(1) if match else None


def required(tag):
    # Ignore text in quoted attribute values such as title="required field".
    without_values = re.sub(r"""=\s*(?:"[^"]*"|'[^']*')""", '=""', tag)
    return bool(re.search(r"(?<![\w:-])required(?=\s|=|>|$)", without_values, re.I))


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
            self.current = {"attrs": attrs, "fields": [], "bypass_controls": []}
            self.forms.append(self.current)
            self.ancestors = []
        elif self.current is not None:
            if "formnovalidate" in attrs and (tag == "button" and attrs.get("type", "submit").lower() == "submit" or tag == "input" and attrs.get("type", "").lower() in ("submit", "image")):
                self.current["bypass_controls"].append(tag)
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



def check_form(html, slug, city):
    problems = []
    forms = FORM_RE.findall(html)
    if len(forms) != 1:
        return [f"{slug}: expected exactly one pickup form (found {len(forms)})"]
    form = forms[0]
    opening_tag = form.split(">", 1)[0] + ">"
    if attribute(opening_tag, "action") != "https://formspree.io/f/mvzeapzd":
        problems.append(f"{slug}: form action must match the exact Formspree endpoint")
    if (attribute(opening_tag, "method") or "").lower() != "post":
        problems.append(f"{slug}: pickup requests must be submitted via POST")
    reader = FormReader()
    reader.feed(form)
    parsed_form = reader.forms[0]
    if "novalidate" in parsed_form["attrs"] or parsed_form["bypass_controls"]:
        problems.append(f"{slug}: native required field validation must be enabled")
    for item in parsed_form["fields"]:
        if item["attrs"].get("name") in {
            "source_page", "state", "service", "city", "name", "phone",
            "address", "zip", "appliance", "condition", "location", "stairs"
        } and item["effectively_disabled"]:
            problems.append(f"{slug}: {item['attrs'].get('name')} is disabled and omitted from submissions")
    parsed_fields = {field["attrs"].get("name"): field for field in parsed_form["fields"] if field["tag"] == "select"}
    inputs = INPUT_RE.findall(form)
    selects = [(attrs, options) for attrs, options in SELECT_RE.findall(form)]
    fields = [attribute(tag, "name") for tag in inputs]
    fields += [attribute("<select " + attrs + ">", "name") for attrs, _ in selects]
    fields += [attribute(tag, "name") for tag in re.findall(r"<textarea\b[^>]*>", form, re.I)]
    for field in ("name", "phone", "address", "zip", "appliance", "condition", "location", "stairs"):
        if fields.count(field) != 1:
            problems.append(f"{slug}: {field} must occur exactly once")
    for field, value in (
        ("source_page", slug + "-washer-dryer-pickup"),
        ("state", "California"),
        ("service", "Washer and dryer pickup"),
    ):
        matches = [tag for tag in inputs if attribute(tag, "name") == field]
        if len(matches) != 1 or attribute(matches[0], "value") != value or attribute(matches[0], "type") != "hidden":
            problems.append(f"{slug}: missing or incorrect hidden {field} attribution")
    # Some pages use a static hidden city; Banning/Beaumont already have a
    # native required visible city with the correct default. Preserve both.
    city_inputs = [tag for tag in inputs if attribute(tag, "name") == "city"]
    if len(city_inputs) != 1 or attribute(city_inputs[0], "value") != city or (
        attribute(city_inputs[0], "type") != "hidden" and not required(city_inputs[0])
    ):
        problems.append(f"{slug}: missing or incorrect city attribution")
    for field in ("name", "phone", "address", "zip"):
        matches = [tag for tag in inputs if attribute(tag, "name") == field]
        if len(matches) != 1 or not required(matches[0]):
            problems.append(f"{slug}: {field} must be required")
    for field in ("appliance", "condition", "location", "stairs"):
        found = [(attrs, options) for attrs, options in selects
                 if attribute("<select " + attrs + ">", "name") == field]
        if len(found) != 1:
            problems.append(f"{slug}: {field} must be one native select control")
            continue
        attrs, options = found[0]
        if not required("<select " + attrs + ">"):
            problems.append(f"{slug}: {field} selector must be required")
        first = OPTION_RE.search(options)
        if not first or attribute(first.group(), "value") != "":
            problems.append(f"{slug}: {field} selector must start with a blank-value prompt")
        # A later selected option silently chooses a real answer even if the
        # first option is empty; native required validation would not fire.
        parsed_options = OptionAttributes()
        parsed_options.feed(options)
        if any("selected" in attrs for attrs in parsed_options.options[1:]):
            problems.append(f"{slug}: {field} has a nonblank selected default")
        parsed_select = parsed_fields.get(field)
        if parsed_select:
            options_data = parsed_select["options"]
            if options_data and options_data[0]["attrs"].get("value") == "" and (
                options_data[0]["effectively_disabled"]
                and "selected" not in options_data[0]["attrs"]
            ):
                problems.append(f"{slug}: disabled blank prompt must be explicitly selected")
            if field in ("location", "stairs") and not any(
                ("unknown" in op["text"].lower() or "not sure" in op["text"].lower())
                and not op["effectively_disabled"]
                and op["attrs"].get("value", op["text"].strip()) != ""
                for op in options_data[1:]
            ):
                problems.append(f"{slug}: {field} needs an enabled nonblank unknown option")
    return problems


def self_test():
    slug = "eastvale"
    city = "Eastvale"
    fixed = '<form action="https://formspree.io/f/mvzeapzd" method="POST">'
    for key, value in (("source_page", slug + "-washer-dryer-pickup"),
                       ("state", "California"), ("city", city),
                       ("service", "Washer and dryer pickup")):
        fixed += f'<input type="hidden" name="{key}" value="{value}">'
    for field in ("name", "phone", "address", "zip"):
        fixed += f'<input name="{field}" required>'
    for field in ("appliance", "condition", "location", "stairs"):
        fixed += f'<select name="{field}" required><option value="">Select</option><option>Unknown / not sure</option></select>'
    fixed += '</form>'
    assert check_form(fixed, slug, city) == [], "hidden-city positive fixture failed"
    title_only = fixed.replace('<option>Unknown / not sure</option>',
                               '<option title="Previously selected answer">Unknown / not sure</option>', 1)
    assert check_form(title_only, slug, city) == [], "quoted selected text is not a selected attribute"
    visible_city = fixed.replace(
        '<input type="hidden" name="city" value="Eastvale">',
        '<input name="city" value="Eastvale" required>',
    )
    assert check_form(visible_city, slug, city) == [], "visible-required-city positive fixture failed"
    assert check_form(
        visible_city.replace('<input name="city" value="Eastvale" required>',
                             '<input name="city" value="Eastvale">'),
        slug, city,
    ), "optional visible city escaped"
    negative = [
        fixed.replace('method="POST"', 'method="GET"'),
        fixed.replace(' method="POST"', ''),
        fixed.replace('method="POST"', 'method="POST" novalidate'),
        fixed.replace('</form>', '<button type="submit" formnovalidate>Send</button></form>'),
        fixed.replace('<select name="location" required>', '<select name="location" title="required field">'),
        fixed.replace('name="location" required', 'name="location" required disabled'),
        fixed.replace('<select name="location" required>',
                      '<fieldset disabled><select name="location" required>')
             .replace('</select><select name="stairs" required>',
                      '</select></fieldset><select name="stairs" required>'),
        fixed.replace('name="source_page"', 'name="source_page" disabled'),
        fixed.replace('name="phone" required', 'name="phone" required disabled'),
        fixed.replace('<option value="">Select</option>', '<option value="" disabled>Select</option>', 1),
        fixed.replace('<option>Unknown / not sure</option>', '<option disabled>Unknown / not sure</option>', 1),
        fixed.replace('<option>Unknown / not sure</option>', '<option value="">Unknown / not sure</option>', 1),
        fixed.replace('<option>Unknown / not sure</option></select><select name="stairs"',
                      '<optgroup disabled label="Other"><option>Unknown / not sure</option></optgroup></select><select name="stairs"'),

        fixed.replace('name="location" required', 'name="location"'),
        fixed.replace('<select name="stairs" required><option value="">',
                      '<select name="stairs" required><option value="none">'),
        fixed.replace('name="city" value="Eastvale"', 'name="city" value=""'),
        fixed.replace('<select name="location" required><option value="">Select</option><option>Unknown / not sure</option></select>', ''),
        fixed.replace('name="source_page"', 'name="source_missing"'),
        fixed.replace('name="location" required', 'data-name="location" required'),
        fixed.replace('name="location" required', 'name="location" data-required="true"'),
        fixed.replace('https://formspree.io/f/mvzeapzd"', 'https://formspree.io/f/mvzeapzd-typo"'),
        fixed.replace(
            '<select name="location" required><option value="">Select</option><option>Unknown / not sure</option></select>',
            '<input name="location" required>',
        ),
        fixed.replace(
            '<select name="location" required><option value="">Select</option><option>Unknown / not sure</option></select>',
            '<select name="location" required><option value="">Select</option><option selected>Unknown / not sure</option></select>',
        ),
    ]
    for i, broken in enumerate(negative, 1):
        assert check_form(broken, slug, city), f"negative fixture {i} escaped"
    print(f"PASS: three positive fixtures and {len(negative)+1} negative intake regressions")


def main():
    self_test()
    failures = []
    for slug, city in CITIES.items():
        path = Path(slug + "-washer-dryer-pickup") / "index.html"
        if not path.is_file():
            failures.append(f"{slug}: missing existing laundry page")
            continue
        failures += check_form(path.read_text(encoding="utf-8"), slug, city)
    if failures:
        print("\n".join(failures))
        sys.exit(1)
    print(f"PASS: {len(CITIES)} existing Inland Empire laundry intake forms validated without any form submission")


if __name__ == "__main__":
    main()
