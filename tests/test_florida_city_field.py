"""Safety regressions for Florida pickup-city request forms."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "florida_audit", ROOT / "scripts" / "audit-florida-major-markets.py"
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def page_for(city_markup):
    html = "<form action='https://formspree.io/f/test'>" + city_markup + "</form>"
    page = audit.Page()
    page.feed(html)
    return page, html


class FloridaPickupCityTests(unittest.TestCase):
    def valid(self, markup, city="Jacksonville", kind="appliance"):
        page, html = page_for(markup)
        return audit.valid_city_field(page, html, city, kind)

    def test_blank_required_actual_city_accepted(self):
        self.assertTrue(self.valid(
            '<label>Actual pickup city'
            '<input name="city" value="" autocomplete="address-level2" '
            'placeholder="Actual pickup city" required></label>'
        ))

    def test_visible_label_with_attributes_accepted(self):
        self.assertTrue(self.valid(
            '<label class="field">Actual pickup city'
            '<input type="text" id="pickup-city" name="city" value="" '
            'placeholder="Actual pickup city" required></label>'
        ))

    def test_legacy_prefilled_city_is_temporary_compatibility(self):
        self.assertTrue(self.valid(
            '<label>Actual pickup city<input name="city" value="Jacksonville" required></label>'
        ))
        self.assertFalse(self.valid(
            '<label>Actual pickup city<input name="city" value="Tampa" required></label>'
        ))

    def test_hidden_disabled_readonly_or_optional_field_rejected(self):
        fields = [
            '<input type="hidden" name="city" value="" placeholder="Actual pickup city" required>',
            '<input name="city" value="" placeholder="Actual pickup city" required disabled>',
            '<input name="city" value="" placeholder="Actual pickup city" required readonly>',
            '<input name="city" value="" placeholder="Actual pickup city">',
        ]
        for field in fields:
            with self.subTest(field=field):
                self.assertFalse(self.valid('<label>Actual pickup city' + field + '</label>'))

    def test_wrong_or_missing_label_rejected(self):
        for label in ("City", "Where is it?"):
            self.assertFalse(self.valid(
                '<label>' + label
                + '<input name="city" value="" placeholder="Actual pickup city" required></label>'
            ))

    def test_data_name_spoof_rejected(self):
        self.assertFalse(self.valid(
            '<input name="city" value="" placeholder="Actual pickup city" required>'
            '<label>Actual pickup city'
            '<input data-name="city" value="" required></label>'
        ))

    def test_duplicate_city_inputs_rejected(self):
        self.assertFalse(self.valid(
            '<label>Actual pickup city'
            '<input name="city" value="" placeholder="Actual pickup city" required></label>'
            '<input name="city" value="Tampa">'
        ))

    def test_all_other_city_guides_keep_exact_city_requirement(self):
        self.assertTrue(self.valid(
            '<label>Actual pickup city<input name="city" value="Orlando" required></label>',
            city="Orlando"
        ))
        self.assertFalse(self.valid(
            '<label>Actual pickup city'
            '<input name="city" value="" placeholder="Actual pickup city" required></label>',
            city="Orlando"
        ))
        self.assertFalse(self.valid(
            '<label>Actual pickup city<input name="city" value="Tampa" required></label>',
            city="Jacksonville", kind="freezer"
        ))


if __name__ == "__main__":
    unittest.main()
