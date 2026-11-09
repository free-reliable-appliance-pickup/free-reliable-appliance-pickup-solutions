"""Offline regressions for the Minnesota live read-only smoke parser."""
import io
import json
import tempfile
import threading
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from scripts.ttg_minnesota_live_smoke import BASE, FORM, REQUIRED, audit_live_page, check_page, has_minnesota_hub_link, main


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
    def test_minnesota_workflow_readiness_target(self):
        """Prevent the Minnesota workflow from auditing a different state."""
        path = Path(__file__).resolve().parents[1] / ".github/workflows/ttg-minnesota-live-smoke.yml"
        workflow = path.read_text(encoding="utf-8")
        self.assertIn("--state MN --report ttg-minnesota-readiness.json", workflow)
        self.assertNotIn("--state IL", workflow)

    def test_audit_page_is_read_only(self):
        """Read a page exactly once through the GET-only fetch helper."""
        with patch("scripts.ttg_minnesota_live_smoke.fetch_html",
                   return_value=fixture()) as get:
            slug, errors = audit_live_page("minnesota-appliance-pickup/index.html", [])
        self.assertEqual(slug, "minnesota-appliance-pickup")
        self.assertEqual(errors, [])
        get.assert_called_once_with("minnesota-appliance-pickup/")

    def test_audit_page_reports_timeout(self):
        """Record network timeouts as failures without stopping other checks."""
        with patch("scripts.ttg_minnesota_live_smoke.fetch_html",
                   side_effect=RuntimeError("timed out")):
            slug, errors = audit_live_page("minneapolis-mn-appliance-pickup/index.html", [])
        self.assertEqual(slug, "minneapolis-mn-appliance-pickup")
        self.assertEqual(errors, ["timed out"])

    def test_main_limits_get_workers_and_preserves_manifest_order(self):
        """Six mocked pages overlap at four workers while reporting in input order."""
        paths = [f"city-{i}-mn-appliance-pickup/index.html" for i in range(6)]
        barrier = threading.Barrier(4)
        lock = threading.Lock()
        active = 0
        peak = 0
        completed = []

        def fake_audit(path, manifest_pages):
            nonlocal active, peak
            self.assertEqual(manifest_pages, paths)
            with lock:
                active += 1
                peak = max(peak, active)
            if path in paths[:4]:
                barrier.wait(timeout=3)
            # Force the first manifest page to finish later than the others.
            time.sleep(0.08 if path == paths[0] else 0.005)
            with lock:
                completed.append(path)
                active -= 1
            return path.removesuffix("/index.html"), []

        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "data/ttg-state-batches/MN.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({"pages": paths}), encoding="utf-8")
            output = io.StringIO()
            with patch("scripts.ttg_minnesota_live_smoke.ROOT", Path(directory)), \\
                 patch("scripts.ttg_minnesota_live_smoke.audit_live_page",
                       side_effect=fake_audit), \\
                 patch("scripts.ttg_minnesota_live_smoke.fetch_html",
                       return_value='<a href="/minnesota-appliance-pickup/">Minnesota</a>'), \\
                 redirect_stdout(output):
                self.assertEqual(main(), 0)

        self.assertEqual(peak, 4)
        self.assertNotEqual(completed, paths)
        reported = [line for line in output.getvalue().splitlines() if line.startswith("PASS ")]
        self.assertEqual(reported, [f"PASS {BASE}{p.removesuffix('/index.html')}/" for p in paths])

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
            "minnesota-appliance-pickup/index.html", "minneapolis-mn-appliance-pickup/index.html"])
        self.assertTrue(any("missing Minnesota hub link" in s for s in errors))

    def test_source_page_mismatch(self):
        """Reject attribution to an unrelated Minnesota landing page."""
        errors = check_page("minneapolis-mn-appliance-pickup", fixture())
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
