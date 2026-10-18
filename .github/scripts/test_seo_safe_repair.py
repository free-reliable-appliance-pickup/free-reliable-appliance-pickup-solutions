#!/usr/bin/env python3
"""Unit tests for conservative SEO repair behavior."""
import importlib.util
import pathlib
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = pathlib.Path(__file__).with_name("seo_safe_repair.py")
spec = importlib.util.spec_from_file_location("seo_safe_repair", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class RepairTests(unittest.TestCase):
    def test_only_unambiguous_missing_html_link_is_repaired(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "destination.html").write_text("OK")
            (root / "existing").mkdir()
            (root / "existing" / "index.html").write_text("OK")
            source = root / "index.html"
            source.write_text(
                '<a href="/destination">fix</a>'
                '<a href="/existing">keep</a>'
                '<a href="https://elsewhere.example/destination">external</a>'
                '<a href="/missing">unknown</a>'
                '<a href="tel:6148743407">call</a>'
            )
            with patch.object(module, "ROOT", root):
                self.assertEqual(len(module.repair(source)), 1)
                self.assertIn('href="/destination"', source.read_text())
                module.repair(source, dry_run=False)
                result = source.read_text()
                self.assertIn('href="/destination.html"', result)
                self.assertIn('href="/existing"', result)
                self.assertIn('href="tel:6148743407"', result)
                self.assertEqual(module.repair(source, dry_run=False), [])

if __name__ == "__main__":
    unittest.main()
