import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_indiana_gold_grid():
    data = json.loads((ROOT / "data/ttg-state-batches/IN.json").read_text(encoding="utf-8"))
    paths = data["pages"]
    assert data["mode"] == "request-only"
    assert data["operator_coverage_verified"] is False
    assert len(paths) == len(set(paths)) == 251
    for kind, count in [("appliance",51),("washer-dryer",50),("refrigerator",50),("stove-oven",50),("freezer",50)]:
        assert sum(p.endswith(f"-{kind}-pickup/index.html") for p in paths) == count
    for path in paths:
        html = (ROOT / path).read_text(encoding="utf-8")
        assert 'noindex, follow' in html, path
        assert 'Free Reliable Appliance Pickup' in html, path
        assert 'https://formspree.io/f/mvzeapzd' in html, path
        assert '<img' in html and '<form' in html, path
        assert '<h1' in html, path
    hub = (ROOT / "indiana-appliance-pickup/index.html").read_text(encoding="utf-8")
    assert hub.index("<form") < hub.index("Free Appliance Pickup Locations in Indiana")
    assert '/mccordsville-in-freezer-pickup/' in hub
