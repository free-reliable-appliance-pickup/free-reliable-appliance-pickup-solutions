"""Offline regressions for the Illinois live read-only smoke parser."""
import unittest
from scripts.ttg_illinois_live_smoke import BASE, FORM, REQUIRED, check_page, has_illinois_hub_link


def fixture(slug="illinois-appliance-pickup", robots="noindex, follow"):
    """Return a complete minimal Illinois request-form page fixture."""
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
    """Verify Illinois form, canonical, robots, and navigation requirements."""
    def test_valid_request_only(self):
        """Accept a fully valid request-only page."""
        self.assertEqual(check_page("illinois-appliance-pickup", fixture()), [])

    def test_index_leak_blocked(self):
        """Reject an indexable page before local pickup coverage is verified."""
        self.assertTrue(any("noindex" in s for s in check_page(
            "illinois-appliance-pickup", fixture(robots="index, follow"))))

    def test_missing_hub_link(self):
        """Report missing city links on the statewide Illinois hub."""
        errors = check_page("illinois-appliance-pickup", fixture(), [
            "illinois-appliance-pickup/index.html", "chicago-il-appliance-pickup/index.html"])
        self.assertTrue(any("missing Illinois hub link" in s for s in errors))

    def test_source_page_mismatch(self):
        """Reject attribution to an unrelated Illinois landing page."""
        errors = check_page("chicago-il-appliance-pickup", fixture())
        self.assertTrue(any("source_page mismatch" in s for s in errors))

    def test_no_required_field_failure(self):
        """Reject missing required intake fields."""
        bad = fixture().replace('<input name="zip" required>', '<input name="zip">')
        self.assertTrue(any("nonrequired zip" in s for s in check_page(
            "illinois-appliance-pickup", bad)))

    def test_service_areas_relative_root_and_absolute_links(self):
        """Recognize all supported Illinois hub link forms."""
        urls = (
            "../illinois-appliance-pickup/",
            "/illinois-appliance-pickup/",
            BASE + "illinois-appliance-pickup/",
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(has_illinois_hub_link('<a href="' + url + '">Illinois</a>'))

    def test_service_areas_missing_and_external_links(self):
        """Reject no link and off-site lookalike URLs."""
        self.assertFalse(has_illinois_hub_link("<p>No Illinois directory listing</p>"))
        self.assertFalse(has_illinois_hub_link(
            '<a href="https://elsewhere.example/illinois-appliance-pickup/">Illinois</a>'
        ))


if __name__ == "__main__":
    unittest.main()
