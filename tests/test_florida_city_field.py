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

    def test_valid_name_attribute_spellings(self):
        variants = ("name='city'", "name=city", 'name = "city"')
        for name_attribute in variants:
            with self.subTest(name_attribute=name_attribute):
                self.assertTrue(self.valid(
                    '<label class="field">Actual pickup city'
                    '<input ' + name_attribute
                    + ' value="" placeholder="Actual pickup city" required></label>'
                ))

    def test_valueless_type_attribute_does_not_crash(self):
        self.assertTrue(self.valid(
            '<label>Actual pickup city'
            '<input type name="city" value="" placeholder="Actual pickup city" required></label>'
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

    def test_lookalike_label_outside_form_rejected(self):
        field = '<input name="city" value="" placeholder="Actual pickup city" required>'
        fake_label = '<label>Actual pickup city' + field + '</label>'
        html = fake_label + '<form action="https://formspree.io/f/test">' + field + '</form>'
        page = audit.Page()
        page.feed(html)
        self.assertFalse(audit.valid_city_field(page, html, "Jacksonville", "appliance"))

    def test_lookalike_label_in_html_comment_rejected(self):
        field = '<input name="city" value="" placeholder="Actual pickup city" required>'
        html = ('<form action="https://formspree.io/f/test">'
                '<!-- <label>Actual pickup city' + field + '</label> -->'
                + field + '</form>')
        page = audit.Page()
        page.feed(html)
        self.assertFalse(audit.valid_city_field(page, html, "Tampa", "appliance"))

    def test_lookalike_label_inside_template_rejected(self):
        field = '<input name="city" value="" placeholder="Actual pickup city" required>'
        html = ('<form action="https://formspree.io/f/test">'
                '<template><label>Actual pickup city' + field + '</label></template>'
                + field + '</form>')
        page = audit.Page()
        page.feed(html)
        self.assertFalse(audit.valid_city_field(page, html, "Tallahassee", "appliance"))

    def test_inert_template_form_cannot_terminate_real_form(self):
        self.assertTrue(self.valid(
            '<template><form><input name="city" value="Incorrect"></form></template>'
            '<label>Actual pickup city'
            '<input name="city" value="" placeholder="Actual pickup city" required></label>'
        ))

    def test_hidden_label_rejected(self):
        for hidden in ('hidden', 'style="display: none"', 'aria-hidden="true"'):
            with self.subTest(hidden=hidden):
                self.assertFalse(self.valid(
                    '<label ' + hidden + '>Actual pickup city'
                    '<input name="city" value="" placeholder="Actual pickup city" required></label>'
                ))

    def test_label_for_must_point_to_the_city_field(self):
        self.assertFalse(self.valid(
            '<label for="zip">Actual pickup city'
            '<input id="pickup-city" name="city" value="" '
            'placeholder="Actual pickup city" required></label>'
        ))
        self.assertFalse(self.valid(
            '<label for="pickup-city">Actual pickup city'
            '<input name="city" value="" placeholder="Actual pickup city" required></label>'
        ))
        self.assertTrue(self.valid(
            '<label for="pickup-city">Actual pickup city'
            '<input id="pickup-city" name="city" value="" '
            'placeholder="Actual pickup city" required></label>'
        ))

    def test_duplicate_city_inputs_rejected(self):
        self.assertFalse(self.valid(
            '<label>Actual pickup city'
            '<input name="city" value="" placeholder="Actual pickup city" required></label>'
            '<input name="city" value="Tampa">'
        ))

    def test_valid_noindex_follow_in_city_guides(self):
        self.assertTrue(audit.valid_request_robots(["noindex, follow"]))
        self.assertTrue(audit.valid_request_robots([" NoIndex , FOLLOW , noarchive "]))

    def test_conflicting_or_duplicate_robots_rejected(self):
        invalid = (
            [], ["index, follow"], ["notnoindex, follow"],
            ["noindex, index, follow"], ["noindex, nofollow"],
            ["noindex"], ["noindex, follow", "index, follow"],
        )
        for robots in invalid:
            with self.subTest(robots=robots):
                self.assertFalse(audit.valid_request_robots(robots))

    def test_other_cities_reject_hidden_or_unusable_city_controls(self):
        for bad in (
            '<input type="hidden" name="city" value="Orlando" required>',
            '<input name="city" value="Orlando" required disabled>',
            '<input name="city" value="Orlando" required readonly>',
            '<input name="city" value="Orlando">',
        ):
            with self.subTest(markup=bad):
                self.assertFalse(self.valid('<label>Actual pickup city' + bad + '</label>',
                                            city="Orlando"))
        self.assertTrue(self.valid(
            '<label>Actual pickup city<input name="city" value="Orlando" required></label>',
            city="Orlando"
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
