"""Tests for TTG source-backed, noindex-only off-repository draft factory."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.ttg_fasttrack_generate import validated_pages, render, main


def make_fixture(root: Path, *, city="Evanston", category="appliance"):
    (root / "data").mkdir(exist_ok=True)
    defaults = [{"state_code": "IL", "state": "Illinois"}]
    (root / "data/market-routing.json").write_text(
        json.dumps({"state_defaults": defaults}), encoding="utf-8")
    (root / "real-used-appliances.webp").write_bytes(b"fixture")
    base = (
        "Evanston's official 311 resource covers special collection separately from "
        "ordinary bulk rubbish. Confirm exact appliance eligibility directly instead of "
        "assuming a new appliance will be removed from an alley by routine collection."
    )
    page = {
        "city": city, "state_code": "IL", "category": category, "mode": "request-only",
        "title": "Evanston, Illinois used appliance pickup eligibility requests",
        "description": "Review used appliance pickup eligibility in Evanston, Illinois; provide condition, access and an address. No pickup crew is confirmed or guaranteed.",
        "local_context": base,
        "access_guidance": "Ask the landlord or condo board about the freight elevator, doorway width, stair landing, and any loading dock or alley restrictions before requesting a heavy appliance movement.",
        "condition_guidance": "For washers, test filling, drainage and spin; for refrigerators check that both compartments cool and photograph their interiors. Include repair needs, floor and quantity for any mixed load.",
        "official_resource_note": "Municipal collection and this website are entirely separate. Evanston residents can ask 311 whether their specific appliance qualifies for a separately arranged collection.",
        "official_resource_url": "https://www.cityofevanston.org/departments/public_works/services/waste_services/special_pick_ups_and_bulk_collection.php",
        "official_resource_label": "City of Evanston special collections and bulk pickup",
        "photo": "/real-used-appliances.webp",
        "photo_alt": "Used laundry and refrigeration machines stored in a garage; illustration, not an Evanston pickup",
    }
    manifest = root / "drafts.json"
    manifest.write_text(json.dumps({"pages": [page]}), encoding="utf-8")
    return manifest, page


class GeneratorTests(unittest.TestCase):
    def test_generated_page_is_noindex_with_qualified_form(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            manifest, _ = make_fixture(root)
            records = validated_pages(root, manifest)
            self.assertEqual(len(records), 1)
            html = render(records[0])
            self.assertIn('name="robots" content="noindex, follow"', html)
            self.assertIn('name="source_page" value="evanston-il-appliance-pickup"', html)
            self.assertIn('value="IL"', html)
            self.assertIn('name="privacy_acknowledgment"', html)
            self.assertIn("https://formspree.io/f/mvzeapzd", html)
            self.assertEqual(html.count("<img "), 1)
            self.assertEqual(html.count("<form "), 1)
            self.assertNotIn("LocalBusiness", html)
            self.assertIn("not a completed Evanston job", html)

    def test_writes_only_to_separate_explicit_review_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            make_fixture(root)
            self.assertEqual(main(["--root", str(root), "--manifest", "drafts.json",
                                   "--output-dir", str(root / "published")]), 1)
            dest = Path(temporary) / "review"
            self.assertEqual(main(["--root", str(root), "--manifest", "drafts.json",
                                   "--output-dir", str(dest)]), 0)
            self.assertTrue((dest / "evanston-il-appliance-pickup/index.html").is_file())
            self.assertEqual(main(["--root", str(root), "--manifest", "drafts.json",
                                   "--output-dir", str(dest)]), 1)

    def test_missing_photo_blocks_generation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            manifest, _ = make_fixture(root)
            (root / "real-used-appliances.webp").unlink()
            with self.assertRaisesRegex(ValueError, "missing/unsafe local photo"):
                validated_pages(root, manifest)

    def test_refuses_unverified_publication_mode(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            manifest, page = make_fixture(root)
            page["mode"] = "live-indexable"
            manifest.write_text(json.dumps({"pages": [page]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "only explicit request-only"):
                validated_pages(root, manifest)

    def test_duplicate_and_existing_site_pages_are_blocked(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            manifest, page = make_fixture(root)
            manifest.write_text(json.dumps({"pages": [page, page]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                validated_pages(root, manifest)
            manifest.write_text(json.dumps({"pages": [page]}), encoding="utf-8")
            existing = root / "evanston-il-appliance-pickup/index.html"
            existing.parent.mkdir()
            existing.write_text("already exists", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "already exists"):
                validated_pages(root, manifest)

    def test_missing_unique_research_section_blocks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            manifest, page = make_fixture(root)
            page["local_context"] = "generic"
            manifest.write_text(json.dumps({"pages": [page]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "local_context must be manually authored"):
                validated_pages(root, manifest)


if __name__ == "__main__":
    unittest.main()
