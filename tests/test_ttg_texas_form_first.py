from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "texas-appliance-pickup" / "index.html").read_text(encoding="utf-8")

def test_texas_customer_request_form_is_first_main_section():
    main_start = HTML.index("<main>")
    first_section = re.search(r"<section\\b[^>]*>", HTML[main_start:])
    assert first_section
    assert 'id="request"' in first_section.group()
    assert HTML.index('id="request"') < HTML.index('id="texas-city-shortcut"')
    assert HTML.index('id="request"') < HTML.index('id="texas-population-priority"')

def test_texas_customer_form_routes_and_safety_preserved():
    assert HTML.count("<form ") == 1
    assert 'action="https://formspree.io/f/mvzeapzd"' in HTML
    assert 'name="source_page" value="texas-appliance-pickup"' in HTML
    assert 'name="state" value="TX"' in HTML
    for field in ("name", "phone", "address", "city", "zip", "condition", "floor", "stairs", "access", "photos_available"):
        assert 'name="' + field + '"' in HTML, field
    assert 'id="texas-quick-continue"' in HTML
    assert 'id="texas-quick-city"' in HTML
