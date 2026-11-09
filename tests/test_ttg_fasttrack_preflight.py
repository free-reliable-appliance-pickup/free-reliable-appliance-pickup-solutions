"""Tests for TTG FastTrack source preflight (never imply live deployment)."""
from pathlib import Path
import tempfile
import unittest

from scripts.ttg_fasttrack_preflight import inspect_page


def create_page(root: Path, *, noindex: bool = True, img_exists: bool = True):
    page = root / "chicago-il-appliance-pickup/index.html"
    page.parent.mkdir(parents=True)
    (root / "assets").mkdir(exist_ok=True)
    if img_exists:
        (root / "assets/real-used-appliances.webp").write_bytes(b"mock-image")
    fields = "".join(
        f'<label>{name}<input name="{name}" required></label>'
        for name in ("name", "phone", "address", "city", "state", "zip",
                     "appliance", "condition", "floor", "stairs",
                     "access", "photos_available")
    )
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    markup = (
        '<!doctype html><html><head><title>Chicago IL appliance eligibility</title>'
        + robots
        + '<link rel="canonical" href="https://freereliableappliancepickup.com/chicago-il-appliance-pickup/">'
        + '</head><body><h1>Chicago Appliance Pickup Requests</h1>'
        + '<p>Chicago is request only; local pickup is not confirmed.</p>'
        + '<img src="/assets/real-used-appliances.webp" alt="Used appliances in a garage">'
        + '<form action="https://formspree.io/f/mvzeapzd" method="POST">'
        + '<input type="hidden" name="source_page" value="chicago-il-appliance-pickup">'
        + fields
        + '<label>Agree<input type="checkbox" required name="privacy_acknowledgment"></label>'
        + '<input type="url" name="photo_link"><button type="submit">Request review</button>'
        + '</form><script src="/assets/customer-routing.js"></script>'
        + '</body></html>'
    )
    page.write_text(markup, encoding="utf-8")
    return "chicago-il-appliance-pickup/index.html"


class PreflightTests(unittest.TestCase):
    def test_valid_request_only_fixture(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            path = create_page(root)
            result = inspect_page(root, path, "IL", request_only=True)
            self.assertEqual(result["errors"], [])
            self.assertTrue(result["passed"])
            self.assertFalse(result["publication_approved"])

    def test_unverified_city_requires_noindex(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            path = create_page(root, noindex=False)
            result = inspect_page(root, path, "IL", request_only=True)
            self.assertIn("request_only_must_be_noindex", result["errors"])
            self.assertFalse(result["passed"])

    def test_missing_image_is_blocking(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            path = create_page(root, img_exists=False)
            result = inspect_page(root, path, "IL", request_only=True)
            self.assertTrue(any(x.startswith("image_asset_not_found") for x in result["errors"]))

    def test_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            result = inspect_page(root, "../outside/index.html", "IL", request_only=True)
            self.assertFalse(result["passed"])
            self.assertTrue(any(x.startswith("unreadable_or_invalid_path") for x in result["errors"]))

    def test_bad_canonical_and_missing_phone_are_blocking(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            path = create_page(root)
            location = root / path
            text = location.read_text(encoding="utf-8")
            text = text.replace("name=\"phone\" required", "name=\"phone\"")
            text = text.replace("freereliableappliancepickup.com", "untrusted.example")
            location.write_text(text, encoding="utf-8")
            result = inspect_page(root, path, "IL", request_only=True)
            self.assertIn("required_attribute_missing:phone", result["errors"])
            self.assertTrue(any(x.startswith("canonical_mismatch") for x in result["errors"]))


if __name__ == "__main__":
    unittest.main()
