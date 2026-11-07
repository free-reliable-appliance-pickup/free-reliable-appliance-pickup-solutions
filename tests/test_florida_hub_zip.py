#!/usr/bin/env python3
"""Read-only regression test for the Florida statewide pickup ZIP field."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "florida-appliance-pickup" / "index.html"


class FormFields(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms = []
        self.form = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "form":
            self.form = {"attrs": attributes, "fields": {}}
            self.forms.append(self.form)
        elif self.form is not None and tag in ("input", "select", "textarea"):
            name = attributes.get("name")
            if name:
                self.form["fields"].setdefault(name, []).append(attributes)

    def handle_endtag(self, tag):
        if tag == "form":
            self.form = None


class FloridaHubZipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = FormFields()
        cls.parser.feed(HUB.read_text(encoding="utf-8"))

    def test_one_customer_request_form_and_one_zip(self):
        self.assertEqual(len(self.parser.forms), 1)
        form = self.parser.forms[0]
        self.assertTrue(form["attrs"].get("action", "").startswith("https://formspree.io/f/"))
        self.assertEqual(form["attrs"].get("method", "").lower(), "post")
        self.assertEqual(len(form["fields"].get("zip", [])), 1)

    def test_zip_input_uses_five_ascii_digits_and_mobile_keyboard(self):
        fields = self.parser.forms[0]["fields"]
        zipfield = fields["zip"][0]
        self.assertEqual(zipfield.get("type"), "text")
        self.assertIn("required", zipfield)
        self.assertEqual(zipfield.get("inputmode"), "numeric")
        self.assertEqual(zipfield.get("autocomplete"), "postal-code")
        self.assertEqual(zipfield.get("pattern"), "[0-9]{5}")
        self.assertEqual(zipfield.get("minlength"), "5")
        self.assertEqual(zipfield.get("maxlength"), "5")
        for valid in ("33101", "32801", "02108"):
            with self.subTest(valid=valid):
                self.assertIsNotNone(re.fullmatch(zipfield["pattern"], valid))
        for invalid in ("", "3310", "331011", "ABCDE", "3310A", "33 01"):
            with self.subTest(invalid=invalid):
                self.assertIsNone(re.fullmatch(zipfield["pattern"], invalid))

    def test_city_address_and_phone_remain_required(self):
        fields = self.parser.forms[0]["fields"]
        for name in ("name", "phone", "address", "city", "floor", "stairs", "condition", "photos_available"):
            with self.subTest(name=name):
                self.assertEqual(len(fields.get(name, [])), 1)
                self.assertIn("required", fields[name][0])

    def test_no_form_upload_claims(self):
        fields = self.parser.forms[0]["fields"]
        self.assertTrue(fields.get("photo_link"))
        self.assertFalse(any(f.get("type") == "file" for group in fields.values() for f in group))


if __name__ == "__main__":
    unittest.main()
