"""Offline regressions for the Illinois live read-only smoke parser."""
import unittest
from scripts.ttg_illinois_live_smoke import BASE, FORM, REQUIRED, check_page


def fixture(slug="illinois-appliance-pickup", robots="noindex, follow"):
    inputs = "".join('<input name="%s" required>' % name for name in REQUIRED if name != "state")
    return (
        '<html><head><meta name="robots" content="%s">' % robots
        + '<link rel="canonical" href="' + BASE + slug + '/">'
        + '<script src="/assets/customer-routing.js"></script></head><body><h1>Request</h1>'
        + '<img src="/photo.webp" alt="Used appliance photograph">'
        + '<a href="/privacy/">Privacy policy</a>'
        + '<form method="POST" action="' + FORM + '">'
        + inputs
        + '<input name="source_page" value="' + slug + '">'
        + '<select name="state" required><option value="">Choose</option><option value="IL">Illinois</option></select>'
        + '</form></body></html>'
    )


class SmokeRegression(unittest.TestCase):
    def test_valid_request_only(self):
        self.assertEqual(check_page("illinois-appliance-pickup", fixture()), [])

    def test_index_leak_blocked(self):
        self.assertTrue(any("noindex" in s for s in check_page(
            "illinois-appliance-pickup", fixture(robots="index, follow"))))

    def test_missing_hub_link(self):
        errors = check_page("illinois-appliance-pickup", fixture(), [
            "illinois-appliance-pickup/index.html", "chicago-il-appliance-pickup/index.html"])
        self.assertTrue(any("missing Illinois hub link" in s for s in errors))

    def test_source_page_mismatch(self):
        errors = check_page("chicago-il-appliance-pickup", fixture())
        self.assertTrue(any("source_page mismatch" in s for s in errors))

    def test_no_required_field_failure(self):
        bad = fixture().replace('<input name="zip" required>', '<input name="zip">')
        self.assertTrue(any("nonrequired zip" in s for s in check_page(
            "illinois-appliance-pickup", bad)))


if __name__ == "__main__":
    unittest.main()
