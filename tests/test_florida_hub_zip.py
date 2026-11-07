#!/usr/bin/env python3
"""Read-only regression tests for Florida statewide ZIP and access intake."""
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
        self.current_select = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "form":
            self.form = {"attrs": attributes, "fields": {}, "select_options": {}}
            self.forms.append(self.form)
        elif self.form is not None and tag in ("input", "select", "textarea"):
            name = attributes.get("name")
            if name:
                self.form["fields"].setdefault(name, []).append(attributes)
                if tag == "select":
                    self.current_select = name
        elif self.form is not None and tag == "option" and self.current_select:
            self.form["select_options"].setdefault(self.current_select, []).append(attributes)

    def handle_endtag(self, tag):
        if tag == "select":
            self.current_select = None
        elif tag == "form":
            self.form = None
            self.current_select = None


class FloridaHubZipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.markup = HUB.read_text(encoding="utf-8")
        cls.parser = FormFields()
        cls.parser.feed(cls.markup)

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
        self.assertEqual(zipfield.get("aria-describedby"), "florida-zip-help")
        self.assertIn('id="florida-zip-help">Enter a five-digit pickup ZIP code', self.markup)
        self.assertIn("required for routing, not a guaranteed appointment", self.markup)
        self.assertEqual(zipfield.get("minlength"), "5")
        self.assertEqual(zipfield.get("maxlength"), "5")
        for valid in ("33101", "32801", "02108"):
            with self.subTest(valid=valid):
                self.assertIsNotNone(re.fullmatch(zipfield["pattern"], valid))
        for invalid in ("", "3310", "331011", "ABCDE", "3310A", "33 01"):
            with self.subTest(invalid=invalid):
                self.assertIsNone(re.fullmatch(zipfield["pattern"], invalid))

    def test_contact_location_and_access_are_required(self):
        fields = self.parser.forms[0]["fields"]
        for name in ("name", "phone", "address", "city", "zip", "appliance", "floor", "stairs", "condition", "photos_available", "access", "message"):
            with self.subTest(name=name):
                self.assertEqual(len(fields.get(name, [])), 1)
                self.assertIn("required", fields[name][0])

    def test_required_selects_have_no_default_answer(self):
        form = self.parser.forms[0]
        for name in ("appliance", "condition", "floor", "stairs", "photos_available"):
            with self.subTest(name=name):
                self.assertIn("required", form["fields"][name][0])
                options = form["select_options"].get(name, [])
                self.assertGreater(len(options), 1)
                selected = [opt for opt in options if "selected" in opt]
                self.assertLessEqual(len(selected), 1)
                default = selected[0] if selected else options[0]
                self.assertEqual(default.get("value"), "", name + " must require a deliberate choice")

    def test_access_guidance_is_visible_and_linked_to_input(self):
        access = self.parser.forms[0]["fields"]["access"][0]
        self.assertEqual(access.get("type"), "text")
        self.assertEqual(access.get("aria-describedby"), "florida-access-help")
        self.assertNotIn("If none", access.get("placeholder", ""))
        self.assertRegex(
            self.markup,
            r'<p class="site-request-note" id="florida-access-help">[^<]*enter "None"[^<]*</p>',
        )

    def test_appliance_inventory_is_required_and_guidance_stays_visible(self):
        details = self.parser.forms[0]["fields"]["message"]
        self.assertEqual(len(details), 1)
        self.assertIn("required", details[0])
        self.assertEqual(details[0].get("id"), "florida-message")
        message_label = (
            r'<label for="florida-message">Appliance Details \(required\): List each appliance, quantity, '
            r'whether it works, repair problems, and brand/model if known\.'
            r'<textarea\s+id="florida-message" name="message"[^>]*></textarea></label>'
        )
        self.assertRegex(self.markup, message_label)
        # Negative fixture: visible instructions are insufficient when their
        # label is not programmatically associated with the textarea.
        disconnected = self.markup.replace(
            '<label for="florida-message">Appliance Details (required):',
            '<div>Appliance Details (required):',
        ).replace('</textarea></label>', '</textarea></div>')
        self.assertNotRegex(disconnected, message_label)

    def test_no_form_upload_claims(self):
        fields = self.parser.forms[0]["fields"]
        self.assertTrue(fields.get("photo_link"))
        self.assertFalse(any(f.get("type") == "file" for group in fields.values() for f in group))


if __name__ == "__main__":
    unittest.main()
