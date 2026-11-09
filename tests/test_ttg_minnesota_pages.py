"""TTG Minnesota: request-only QA for 40 staged pages, hub navigation and photo assets."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import unittest

from scripts.ttg_state_batch_qa import ROOT, check_manifest, Page

CITIES = (
    "minneapolis", "saint-paul", "bloomington", "brooklyn-park",
    "maple-grove", "blaine", "woodbury", "lakeville", "rosemount",
    "plymouth", "eden-prairie", "burnsville", "rochester", "st-cloud", "duluth"
)
CATEGORY_CITIES = (
    "minneapolis", "saint-paul", "bloomington", "brooklyn-park", "maple-grove", "rochester"
)
KINDS = ("washer-dryer", "refrigerator", "stove-oven", "freezer")


class MinnesotaBatchTests(unittest.TestCase):
    """Protect staged-only service claims, Formspree routing and real assets."""

    @classmethod
    def setUpClass(cls):
        """Read the exact manifest and local HTML checkout."""
        cls.manifest = ROOT / "data/ttg-state-batches/MN.json"
        cls.pages = json.loads(cls.manifest.read_text(encoding="utf-8"))["pages"]

    def test_manifest_has_40_pages_with_required_groups(self):
        """One hub, fifteen general city guides and six sets of categories."""
        self.assertEqual(len(self.pages), 40)
        self.assertEqual(len(self.pages), len(set(self.pages)))
        self.assertIn("minnesota-appliance-pickup/index.html", self.pages)
        for city in CITIES:
            self.assertIn(f"{city}-mn-appliance-pickup/index.html", self.pages)
        for city in CATEGORY_CITIES:
            for kind in KINDS:
                self.assertIn(f"{city}-mn-{kind}-pickup/index.html", self.pages)

    def test_standard_ttg_preflight_all_pages(self):
        """No invented pickup route or indexable page can pass the batch."""
        self.assertEqual(check_manifest(self.manifest), [])

    def test_source_state_images_and_form_are_consistent(self):
        """Require matching source pages, one real photo and field protections."""
        for path in self.pages:
            slug = path.removesuffix("/index.html")
            with self.subTest(slug=slug):
                html = (ROOT / path).read_text(encoding="utf-8")
                parser = Page()
                parser.feed(html)
                self.assertEqual(parser.h1, 1)
                self.assertEqual(len(parser.forms), 1)
                self.assertIn("noindex, follow", parser.robots)
                self.assertEqual(parser.fields["source_page"][0].get("value"), slug)
                self.assertEqual(parser.state_options, ["", "MN"])
                self.assertEqual(len(parser.images), 1)
                photo = parser.images[0].get("src", "")
                self.assertTrue((ROOT / photo.lstrip("/")).is_file(), photo)
                self.assertIn("Photo is illustrative, not a completed Minnesota service job.", html)
                self.assertIn("/assets/customer-routing.js", html)
                self.assertIn("/privacy/", html)
                self.assertNotIn('content="index, follow"', html)

    def test_statewide_privacy_acknowledgment_and_photo_are_accurate(self):
        """Preserve explicit privacy consent and avoid invented Minnesota pickup proof."""
        html = (ROOT / "minnesota-appliance-pickup/index.html").read_text(encoding="utf-8")
        self.assertIn("I acknowledge the privacy notice above", html)
        self.assertIn("does not book or guarantee free pickup", html)
        self.assertIn('name="privacy_acknowledgment" value="acknowledged" required', html)
        self.assertIn("illustrative only; not a documented Minnesota pickup", html)
        self.assertIn("<h1>Minnesota Free Appliance Pickup", html)
        self.assertIn('content="noindex, follow"', html)

    def test_hub_links_to_every_city_and_category(self):
        """Ensure Google/crawl navigation has no orphaned staged pages."""
        hub = (ROOT / "minnesota-appliance-pickup/index.html").read_text(encoding="utf-8")
        for path in self.pages:
            slug = path.removesuffix("/index.html")
            if slug == "minnesota-appliance-pickup":
                continue
            with self.subTest(slug=slug):
                self.assertIn(f'href="/{slug}/"', hub)
        for city in CATEGORY_CITIES:
            home = (ROOT / f"{city}-mn-appliance-pickup/index.html").read_text(encoding="utf-8")
            for kind in KINDS:
                self.assertIn(f'/{city}-mn-{kind}-pickup/', home)

    def test_stove_requires_fuel_and_disconnection_status(self):
        """A gas range must never be treated like an unplugged electric range."""
        for city in CATEGORY_CITIES:
            html = (ROOT / f"{city}-mn-stove-oven-pickup/index.html").read_text(encoding="utf-8")
            parser = Page()
            parser.feed(html)
            for field in ("fuel_type", "connection_status"):
                with self.subTest(city=city, field=field):
                    values = parser.fields.get(field, [])
                    self.assertEqual(len(values), 1)
                    self.assertIn("required", values[0])
            self.assertIn("Do not loosen or disconnect a gas line", html)

    def test_service_areas_has_request_only_minnesota_link(self):
        """Keep active service coverage separate from a staging link."""
        service = (ROOT / "service-areas/index.html").read_text(encoding="utf-8")
        self.assertIn("../minnesota-appliance-pickup/", service)
        self.assertIn("Minnesota — free appliance pickup eligibility requests", service)

    def test_minneapolis_and_saint_paul_official_disposal_resources(self):
        """Keep city disposal guidance useful, source-linked and distinct from our unconfirmed request."""
        minneapolis = (ROOT / "minneapolis-mn-appliance-pickup/index.html").read_text(encoding="utf-8")
        saint_paul = (ROOT / "saint-paul-mn-appliance-pickup/index.html").read_text(encoding="utf-8")
        self.assertIn("minneapolismn.gov/resident-services/garbage-recycling-cleanup/large-items/", minneapolis)
        self.assertIn("hennepincounty.gov/green-disposal-guide/items/appliances", minneapolis)
        self.assertIn("stpaul.gov/departments/public-works/garbage-and-recycling/residential-collection/bulky-item-collection", saint_paul)
        self.assertIn("July 1, 2026", saint_paul)
        for html, disclosure in (
            (minneapolis, "this program is separate from our conditional private pickup request"),
            (saint_paul, "City collection is separate from our unconfirmed private appliance pickup request"),
        ):
            self.assertIn('content="noindex, follow"', html)
            section = html.partition("<h2>Alternative recycling and removal options</h2>")[2].partition("</section>")[0]
            self.assertTrue(section, "Alternative options section must be present")
            self.assertIn(disclosure, section)

    def test_official_duluth_rochester_bloomington_options(self):
        """Official disposal alternatives must not imply confirmed private pickup coverage."""
        cases = (
            ("duluth", ("https://wlssd.com/disposal-guide/", "https://wlssd.com/hours-facilities/"), "WLSSD recycling is separate from our unconfirmed private appliance pickup request"),
            ("rochester", ("https://www.olmstedcounty.gov/residents/garbage-recycling/recycling-center-plus", "https://www.olmstedcounty.gov/residents/garbage-recycling/disposal-options"), "County drop-off is separate from our conditional private appliance pickup request"),
            ("bloomington", ("https://www.hennepincounty.gov/green-disposal-guide/items/appliances", "https://www.bloomingtonmn.gov/cob/briefing/get-know-your-options-bulky-item-disposal-2025-04-22"), "separate from our unconfirmed private appliance pickup request"),
        )
        for city, urls, disclosure in cases:
            with self.subTest(city=city):
                html = (ROOT / f"{city}-mn-appliance-pickup/index.html").read_text(encoding="utf-8")
                self.assertIn('content="noindex, follow"', html)
                section = html.partition("<h2>Alternative recycling and removal options</h2>")[2].partition("</section>")[0]
                self.assertTrue(section, "Missing alternatives section")
                for url in urls:
                    self.assertIn(url, section)
                self.assertIn(disclosure, section)
                self.assertIn("Free pickup and local routes are not currently confirmed", html)

    def test_no_minnesota_staging_page_in_sitemap(self):
        """Request-only pages should not be put into discovery index sitemaps."""
        main = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for path in self.pages:
            slug = path.removesuffix("/index.html")
            self.assertNotIn(f"https://freereliableappliancepickup.com/{slug}/", main)

    def test_free_appliance_pickup_wording_stays_conditional(self):
        """Use free pickup keywords without promising unverified service."""
        for path in self.pages:
            with self.subTest(path=path):
                html = (ROOT / path).read_text(encoding="utf-8")
                title = html.split("<title>", 1)[1].split("</title>", 1)[0]
                heading = html.split("<h1>", 1)[1].split("</h1>", 1)[0]
                description = html.split('<meta name="description" content="', 1)[1].split('"', 1)[0]
                self.assertIn("Free ", title)
                self.assertIn("Free ", heading)
                self.assertIn("Free appliance pickup eligibility", description)
                self.assertIn("Looking for free appliance pickup?", html)
                self.assertIn("Free pickup and local routes are not currently confirmed", html)
                self.assertIn('content="noindex, follow"', html)

    def test_routing_stays_unverified(self):
        """A code release must never mark Minnesota as operational by accident."""
        routing = json.loads((ROOT / "data/market-routing.json").read_text(encoding="utf-8"))
        rows = [r for r in routing["state_defaults"] if r["state_code"] == "MN"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "request-only")
        ledger = json.loads((ROOT / "data/ttg-release-readiness/MN.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger["verified_cities"], [])
        self.assertFalse(ledger["form_receipt"]["verified"])


if __name__ == "__main__":
    unittest.main()
