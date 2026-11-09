"""Offline regressions for the Minnesota live read-only smoke parser."""
import unittest
from scripts.ttg_minnesota_live_smoke import BASE, FORM, REQUIRED, check_page, has_minnesota_hub_link


def fixture(slug="minnesota-appliance-pickup", robots="noindex, follow"):
    """Return a complete minimal Minnesota request-form page fixture."""
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
        + '<select name="state" required><option value="">Choose</option><option value="MN">Minnesota</option></select>'
        + '</form></body></html>'
    )


class SmokeRegression(unittest.TestCase):
    """Verify Minnesota form, canonical, robots, and navigation requirements."""
    def test_valid_request_only(self):
        """Accept a fully valid request-only page."""
        self.assertEqual(check_page("minnesota-appliance-pickup", fixture()), [])

    def test_index_leak_blocked(self):
        """Reject an indexable page before local pickup coverage is verified."""
        self.assertTrue(any("noindex" in s for s in check_page(
            "minnesota-appliance-pickup", fixture(robots="index, follow"))))

    def test_missing_hub_link(self):
        """Report missing city links on the statewide Minnesota hub."""
        errors = check_page("minnesota-appliance-pickup", fixture(), [
            "minnesota-appliance-pickup/index.html", "chicago-il-appliance-pickup/index.html"])
        self.assertTrue(any("missing Minnesota hub link" in s for s in errors))

    def test_source_page_mismatch(self):
        """Reject attribution to an unrelated Minnesota landing page."""
        errors = check_page("chicago-il-appliance-pickup", fixture())
        self.assertTrue(any("source_page mismatch" in s for s in errors))

    def test_no_required_field_failure(self):
        """Reject missing required intake fields."""
        bad = fixture().replace('<input name="zip" required>', '<input name="zip">')
        self.assertTrue(any("nonrequired zip" in s for s in check_page(
            "minnesota-appliance-pickup", bad)))

    def test_service_areas_relative_root_and_absolute_links(self):
        """Recognize all supported Minnesota hub link forms."""
        urls = (
            "../minnesota-appliance-pickup/",
            "/minnesota-appliance-pickup/",
            BASE + "minnesota-appliance-pickup/",
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(has_minnesota_hub_link('<a href="' + url + '">Minnesota</a>'))

    def test_service_areas_missing_and_external_links(self):
        """Reject no link and off-site lookalike URLs."""
        self.assertFalse(has_minnesota_hub_link("<p>No Minnesota directory listing</p>"))
        self.assertFalse(has_minnesota_hub_link(
            '<a href="https://elsewhere.example/minnesota-appliance-pickup/">Minnesota</a>'
        ))


if __name__ == "__main__":
    unittest.main()
