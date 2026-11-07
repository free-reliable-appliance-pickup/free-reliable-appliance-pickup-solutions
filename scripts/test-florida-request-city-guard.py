#!/usr/bin/env python3
"""Focused offline regressions for Florida request-city and indexing guards.

Tests the audit parser without contacting Formspree or changing a live page.
The staged city-field migration must accept only the three approved legacy
general-page controls or an explicit required, blank pickup city.
"""
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parent.parent
AUDIT = runpy.run_path(str(ROOT / "scripts/audit-florida-major-markets.py"))
Page = AUDIT["Page"]
valid_city_field = AUDIT["valid_city_field"]
valid_request_robots = AUDIT["valid_request_robots"]


def parse(markup):
    page = Page()
    page.feed(markup)
    return page


def form(input_attrs, label="Actual pickup city", label_attrs="", extra=""):
    return (
        '<form action="https://formspree.io/f/example">'
        f'<label {label_attrs}>{label}<input name="city" {input_attrs}></label>'
        f'{extra}</form>'
    )


class FloridaCityGuardTests(unittest.TestCase):
    def check_city(self, markup, city="Tampa", kind="appliance", expected=True):
        self.assertEqual(
            valid_city_field(parse(markup), markup, city, kind),
            expected,
            msg=f"{city}/{kind}: unexpected validity for {markup}",
        )

    def test_new_blank_actual_pickup_city_is_valid(self):
        self.check_city(form('value="" placeholder="Actual pickup city" required'))

    def test_explicit_city_can_omit_empty_value_attribute(self):
        self.check_city(form('placeholder="Actual pickup city" required'))

    def test_temporary_correct_legacy_city_is_valid(self):
        for city in ("Tampa", "Jacksonville", "Tallahassee"):
            with self.subTest(city=city):
                self.check_city(form(f'value="{city}" required'), city=city)

    def test_wrong_prefilled_city_is_rejected(self):
        self.check_city(form('value="Miami" required'), expected=False)

    def test_unlabelled_real_city_is_rejected(self):
        markup = (
            '<label>Actual pickup city</label><form>'
            '<input name="city" required placeholder="Actual pickup city">'
            '</form>'
        )
        self.check_city(markup, expected=False)

    def test_incorrect_or_hidden_label_is_rejected(self):
        self.check_city(
            form('placeholder="Actual pickup city" required', label="Delivery city"),
            expected=False,
        )
        self.check_city(
            form('placeholder="Actual pickup city" required', label_attrs="hidden"),
            expected=False,
        )

    def test_hidden_readonly_disabled_and_optional_inputs_fail(self):
        for attrs in (
            'type="hidden" placeholder="Actual pickup city" required',
            'placeholder="Actual pickup city" required readonly',
            'placeholder="Actual pickup city" required disabled',
            'placeholder="Actual pickup city"',
        ):
            with self.subTest(attrs=attrs):
                self.check_city(form(attrs), expected=False)

    def test_duplicate_city_field_is_rejected(self):
        self.check_city(
            form(
                'placeholder="Actual pickup city" required',
                extra='<input name="city" value="Tampa" type="hidden">',
            ),
            expected=False,
        )

    def test_template_decoy_does_not_count(self):
        markup = (
            '<template><form><label>Actual pickup city'
            '<input name="city" placeholder="Actual pickup city" required>'
            '</label></form></template>'
            '<form><input name="city" required placeholder="Actual pickup city"></form>'
        )
        self.check_city(markup, expected=False)

    def test_other_cities_keep_real_editable_prefill(self):
        self.check_city(form('value="Miami" required'), city="Miami",
                        kind="washer-dryer", expected=True)
        self.check_city(form('value="Miami" required readonly'), city="Miami",
                        kind="washer-dryer", expected=False)
        self.check_city(form('type="hidden" value="Miami" required'), city="Miami",
                        kind="washer-dryer", expected=False)

    def test_only_unambiguous_noindex_follow_passes(self):
        self.assertTrue(valid_request_robots(["noindex, follow"]))
        self.assertTrue(valid_request_robots(["FOLLOW, NOINDEX"]))
        for directives in (
            [],
            ["index, follow"],
            ["noindex, nofollow"],
            ["index, noindex, follow"],
            ["noindex, follow", "index, follow"],
        ):
            with self.subTest(directives=directives):
                self.assertFalse(valid_request_robots(directives))


if __name__ == "__main__":
    unittest.main()
