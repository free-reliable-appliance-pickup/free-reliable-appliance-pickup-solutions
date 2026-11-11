import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/ttg-state-batches/TN.json"

def test_tennessee_gold_request_only_grid():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pages = payload["pages"]
    assert payload["mode"] == "request-only"
    assert payload["operator_coverage_verified"] is False
    assert len(pages) == len(set(pages)) == 251
    assert sum(p.endswith("-appliance-pickup/index.html") for p in pages) == 51
    assert sum(p.endswith("-washer-dryer-pickup/index.html") for p in pages) == 50
    assert sum(p.endswith("-refrigerator-pickup/index.html") for p in pages) == 50
    assert sum(p.endswith("-stove-oven-pickup/index.html") for p in pages) == 50
    assert sum(p.endswith("-freezer-pickup/index.html") for p in pages) == 50
    for page in pages:
        content = (ROOT / page).read_text(encoding="utf-8")
        assert 'noindex, follow' in content, page
        assert 'Free Reliable Appliance Pickup' in content, page
        assert 'https://formspree.io/f/mvzeapzd' in content, page
        assert '<h1' in content and '<form' in content, page
        assert content.count('<img ') == 1, page
    hub = (ROOT / "tennessee-appliance-pickup/index.html").read_text(encoding="utf-8")
    assert hub.index("<form") < hub.index("Free Appliance Pickup Locations in Tennessee")
