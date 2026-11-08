#!/usr/bin/env python3
"""Regression tests for visible, editable Florida pickup city controls."""
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parent.parent
audit = runpy.run_path(str(ROOT / "scripts/audit-florida-major-markets.py"))
Page = audit["Page"]
valid_city_field = audit["valid_city_field"]


def valid(markup, city="Tampa", kind="appliance"):
    """Parse a synthetic request form and validate the actual city control."""
    page = Page()
    page.feed(markup)
    return valid_city_field(page, markup, city, kind)


class CityFieldVisibilityTests(unittest.TestCase):
    """Reject a city control the customer cannot edit or see."""

    def test_enabled_fieldset_allows_real_city(self):
        """A normal labeled fieldset must remain usable."""
        html = '<form><fieldset><label>Actual pickup city<input name="city" value="" placeholder="Actual pickup city" required></label></fieldset></form>'
        self.assertTrue(valid(html))

    def test_three_major_general_guides_reject_old_prefills(self):
        """Customers must supply their actual city for newly migrated guides."""
        for city in ("Jacksonville", "Tampa", "Tallahassee"):
            html = (
                "<form><label>Actual pickup city"
                f'<input name="city" value="{city}" required></label></form>'
            )
            with self.subTest(city=city):
                self.assertFalse(valid(html, city, "appliance"))

    def test_disabled_fieldset_rejects_city(self):
        """Disabling a parent fieldset must fail for legacy and other guides."""
        for city, kind in (("Tampa", "appliance"), ("Miami", "refrigerator")):
            html = (
                '<form><fieldset disabled><label>Actual pickup city'
                f'<input name="city" value="{city}" required>'
                '</label></fieldset></form>'
            )
            with self.subTest(city=city):
                self.assertFalse(valid(html, city, kind))

    def test_nested_disabled_fieldset_rejects_city(self):
        """Nested enabled fieldsets do not override disabled ancestor controls."""
        html = (
            '<form><fieldset disabled><fieldset><label>Actual pickup city'
            '<input name="city" value="Tampa" required>'
            '</label></fieldset></fieldset></form>'
        )
        self.assertFalse(valid(html))

    def test_hidden_label_rejects_city(self):
        """Hidden label variants cannot satisfy visible-label requirement."""
        for style in ("display: none", "visibility: hidden", " VISIBILITY : HIDDEN "):
            html = (
                '<form><label style="' + style + '">Actual pickup city'
                '<input name="city" value="Tampa" required></label></form>'
            )
            with self.subTest(style=style):
                self.assertFalse(valid(html))


if __name__ == "__main__":
    unittest.main()
