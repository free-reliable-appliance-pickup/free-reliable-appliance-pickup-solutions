from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATES = ["Alaska","Arizona","California","Colorado","Hawaii","Idaho","Montana","Nevada","New Mexico","Oregon","Utah","Washington","Wyoming","Illinois","Indiana","Iowa","Kansas","Michigan","Minnesota","Missouri","Nebraska","North Dakota","Ohio","South Dakota","Wisconsin","Alabama","Arkansas","Florida","Georgia","Kentucky","Louisiana","Mississippi","North Carolina","Oklahoma","South Carolina","Tennessee","Texas","Virginia","West Virginia","Connecticut","Delaware","Maine","Maryland","Massachusetts","New Hampshire","New Jersey","New York","Pennsylvania","Rhode Island","Vermont"]

def test_fifty_state_request_directory():
    html = (ROOT / "service-areas/index.html").read_text(encoding="utf-8")
    start = html.index('class="ttg-fifty-state-request-directory-20261111"')
    end = html.index("</section>", start)
    block = html[start:end]
    assert "Free Appliance Pickup" in block
    assert "not confirmation of service coverage" in block
    assert "eligibility" not in block.lower()
    assert block.count("Free Appliance Pickup requests</a>") == 50
    for name in STATES:
        slug = name.lower().replace(" ", "-")
        assert block.count(f'href="/{slug}-appliance-pickup/"') == 1, name
        assert (ROOT / f"{slug}-appliance-pickup" / "index.html").exists(), name
