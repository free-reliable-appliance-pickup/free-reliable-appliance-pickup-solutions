import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_wisconsin_gold_request_only():
    payload = json.loads((ROOT / "data/ttg-state-batches/WI.json").read_text(encoding="utf-8"))
    pages = payload["pages"]
    assert len(pages) == len(set(pages)) == 251
    assert payload["mode"] == "request-only"
    assert payload["operator_coverage_verified"] is False
    for kind, count in [("-appliance-pickup/",51),("-washer-dryer-pickup/",50),("-refrigerator-pickup/",50),("-stove-oven-pickup/",50),("-freezer-pickup/",50)]:
        assert sum(p.endswith(kind + "index.html") for p in pages) == count
    for page in pages:
        html = (ROOT / page).read_text(encoding="utf-8")
        assert 'noindex, follow' in html, page
        assert 'Free Reliable Appliance Pickup' in html, page
        assert 'https://formspree.io/f/mvzeapzd' in html, page
        assert '<form' in html, page
        assert '<h1' in html, page
        assert '<img' in html, page
    hub = (ROOT / "wisconsin-appliance-pickup/index.html").read_text(encoding="utf-8")
    assert hub.index('<form') < hub.index('Free Appliance Pickup Locations in Wisconsin')
    assert '/deforest-wi-appliance-pickup/' in hub
