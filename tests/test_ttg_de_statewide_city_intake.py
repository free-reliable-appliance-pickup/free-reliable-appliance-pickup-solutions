from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "delaware-appliance-pickup" / "index.html").read_text(encoding="utf-8")

def test_delaware_statewide_intake_city_not_prefilled_as_state():
    form = HTML.split("<form", 1)[1].split("</form>", 1)[0]
    city = re.search(r'<input\b[^>]*\bname="city"[^>]*>', form)
    assert city, "Statewide form must request the actual pickup city"
    field = city.group()
    assert 'required' in field
    assert 'placeholder="Enter actual pickup city or town"' in field
    assert not re.search(r'\bvalue="Delaware"', field)
    assert 'name="state"' in form and 'value="DE"' in form
    assert 'name="zip"' in form and 'name="address"' in form

def test_delaware_statewide_request_copy_and_safety():
    assert "<h2>Request Free Appliance Pickup in Delaware</h2>" in HTML
    assert "in Delaware in Delaware" not in HTML
    assert "DE Free Appliance Pickup request" in HTML
    assert "Request Free Appliance Pickup</button>" in HTML
    assert '<meta name="robots" content="noindex, follow">' in HTML
    assert HTML.count("<form") == 1
