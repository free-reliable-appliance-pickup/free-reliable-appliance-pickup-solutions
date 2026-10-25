#!/usr/bin/env python3
"""VGM: inspect source-only California static paid quote fallback."""
from html.parser import HTMLParser
from pathlib import Path

PAGES = {
    # California regional forms must preserve optional consent without JavaScript.
    "inland-empire-appliance-pickup": "inland-empire-appliance-pickup/index.html",
    "san-gabriel-valley-appliance-pickup": "san-gabriel-valley-appliance-pickup/index.html",
    "riverside-county-appliance-pickup": "riverside-county-appliance-pickup/index.html",
    "san-bernardino-county-appliance-pickup": "san-bernardino-county-appliance-pickup/index.html",
    "san-diego-county-appliance-pickup": "san-diego-county-appliance-pickup/index.html",
    "la-canada-flintridge-appliance-pickup": "la-canada-flintridge-appliance-pickup/index.html",
    "south-pasadena-appliance-pickup": "south-pasadena-appliance-pickup/index.html",
    "victorville-appliance-pickup": "victorville-appliance-pickup/index.html",
    "hesperia-appliance-pickup": "hesperia-appliance-pickup/index.html",
    "adelanto-appliance-pickup": "adelanto-appliance-pickup/index.html",
    "apple-valley-appliance-pickup": "apple-valley-appliance-pickup/index.html",
    "palmdale-appliance-pickup": "palmdale-appliance-pickup/index.html",
    "lancaster-appliance-pickup": "lancaster-appliance-pickup/index.html",
    "palm-springs-appliance-pickup": "palm-springs-appliance-pickup/index.html",
    "palm-desert-appliance-pickup": "palm-desert-appliance-pickup/index.html",
    "la-quinta-appliance-pickup": "la-quinta-appliance-pickup/index.html",
    "rancho-mirage-appliance-pickup": "rancho-mirage-appliance-pickup/index.html",
    # SGV source-only fallback: no JavaScript needed for customer quote preference.
    "pasadena-appliance-pickup": "pasadena-appliance-pickup/index.html",
    "arcadia-appliance-pickup": "arcadia-appliance-pickup/index.html",
    "san-fernando-appliance-pickup": "san-fernando-appliance-pickup/index.html",
    "san-fernando-washer-dryer-pickup": "san-fernando-washer-dryer-pickup/index.html",
    "los-angeles-washer-dryer-pickup": "los-angeles-washer-dryer-pickup/index.html",
    "north-hollywood-appliance-pickup": "north-hollywood-appliance-pickup/index.html",
    "san-fernando-valley-appliance-pickup": "san-fernando-valley-appliance-pickup/index.html",
    "van-nuys-appliance-pickup": "van-nuys-appliance-pickup/index.html",
    "granada-hills-appliance-pickup": "granada-hills-appliance-pickup/index.html",
    "pacoima-appliance-pickup": "pacoima-appliance-pickup/index.html",
    "northridge-appliance-pickup": "northridge-appliance-pickup/index.html",
    "mission-hills-appliance-pickup": "mission-hills-appliance-pickup/index.html",
    "sylmar-appliance-pickup": "sylmar-appliance-pickup/index.html",
    # Other verified California customer forms: same owner-approved no-JS fallback.
    "burbank-appliance-pickup": "burbank-appliance-pickup/index.html",
    "glendale-appliance-pickup": "glendale-appliance-pickup/index.html",
    "calabasas-appliance-pickup": "calabasas-appliance-pickup/index.html",
    "fresno-appliance-pickup": "fresno-appliance-pickup/index.html",
    # Fresno specialty intake must retain no-JS optional quote consent.
    "fresno-washer-dryer-pickup": "fresno-washer-dryer-pickup/index.html",
    # Existing Fresno specialty forms: static no-JS quote choice, never preselected.
    "fresno-refrigerator-pickup": "fresno-refrigerator-pickup/index.html",
    "fresno-freezer-pickup": "fresno-freezer-pickup/index.html",
    "fresno-stove-oven-pickup": "fresno-stove-oven-pickup/index.html",
    "orange-county-appliance-pickup": "orange-county-appliance-pickup/index.html",
    "los-angeles-county-appliance-pickup": "los-angeles-county-appliance-pickup/index.html",
    "anaheim-appliance-pickup": "anaheim-appliance-pickup/index.html",
    "irvine-appliance-pickup": "irvine-appliance-pickup/index.html",
    # Verified existing OC no-JS quote fallback repairs (2026-10-24).
    "santa-ana-appliance-pickup": "santa-ana-appliance-pickup/index.html",
    "lake-forest-appliance-pickup": "lake-forest-appliance-pickup/index.html",
    "ontario-appliance-pickup": "ontario-appliance-pickup/index.html",
    # Five verified Inland Empire laundry form intake corrections, Oct 25.
    "highland-washer-dryer-pickup": "highland-washer-dryer-pickup/index.html",
    "redlands-washer-dryer-pickup": "redlands-washer-dryer-pickup/index.html",
    "eastvale-washer-dryer-pickup": "eastvale-washer-dryer-pickup/index.html",
    "colton-washer-dryer-pickup": "colton-washer-dryer-pickup/index.html",
    "jurupa-valley-washer-dryer-pickup": "jurupa-valley-washer-dryer-pickup/index.html",
    # Existing Inland Empire request forms: approved quote choice works without JS.
    "montclair-appliance-pickup": "montclair-appliance-pickup/index.html",
    "chino-appliance-pickup": "chino-appliance-pickup/index.html",
    "chino-hills-appliance-pickup": "chino-hills-appliance-pickup/index.html",
    "redlands-appliance-pickup": "redlands-appliance-pickup/index.html",
    # Verified IE intake gaps: static quote preference also works without JavaScript.
    "colton-appliance-pickup": "colton-appliance-pickup/index.html",
    "bloomington-appliance-pickup": "bloomington-appliance-pickup/index.html",
    "highland-appliance-pickup": "highland-appliance-pickup/index.html",
    # Verified Riverside County and San Bernardino city no-JS consent gaps (2026-10-24).
    "corona-appliance-pickup": "corona-appliance-pickup/index.html",
    "moreno-valley-appliance-pickup": "moreno-valley-appliance-pickup/index.html",
    "san-bernardino-appliance-pickup": "san-bernardino-appliance-pickup/index.html",
    # Verified Azusa and Irwindale no-JS quote consent gaps (2026-10-24).
    "azusa-appliance-pickup": "azusa-appliance-pickup/index.html",
    "irwindale-appliance-pickup": "irwindale-appliance-pickup/index.html",
    # Verified existing SGV city form no-JS quote gaps (2026-10-24).
    "covina-appliance-pickup": "covina-appliance-pickup/index.html",
    "west-covina-appliance-pickup": "west-covina-appliance-pickup/index.html",
    "el-monte-appliance-pickup": "el-monte-appliance-pickup/index.html",
    "la-puente-appliance-pickup": "la-puente-appliance-pickup/index.html",
    "baldwin-park-appliance-pickup": "baldwin-park-appliance-pickup/index.html",
    "temple-city-appliance-pickup": "temple-city-appliance-pickup/index.html",
    "rosemead-appliance-pickup": "rosemead-appliance-pickup/index.html",
    "monterey-park-appliance-pickup": "monterey-park-appliance-pickup/index.html",
    "san-gabriel-appliance-pickup": "san-gabriel-appliance-pickup/index.html",
    "alhambra-appliance-pickup": "alhambra-appliance-pickup/index.html",
    # Verified San Gabriel Valley no-JS customer quote gaps (2026-10-24).
    "duarte-appliance-pickup": "duarte-appliance-pickup/index.html",
    "monrovia-appliance-pickup": "monrovia-appliance-pickup/index.html",
    "glendora-appliance-pickup": "glendora-appliance-pickup/index.html",
    # Verified Whittier, Montebello and Rialto customer quote-choice gaps (2026-10-24).
    "whittier-appliance-pickup": "whittier-appliance-pickup/index.html",
    "montebello-appliance-pickup": "montebello-appliance-pickup/index.html",
    "rialto-appliance-pickup": "rialto-appliance-pickup/index.html",
    # Verified Southeast Los Angeles County optional quote consent (2026-10-24).
    "pico-rivera-appliance-pickup": "pico-rivera-appliance-pickup/index.html",
    "norwalk-appliance-pickup": "norwalk-appliance-pickup/index.html",
    "downey-appliance-pickup": "downey-appliance-pickup/index.html",
    "la-mirada-appliance-pickup": "la-mirada-appliance-pickup/index.html",
    "cerritos-appliance-pickup": "cerritos-appliance-pickup/index.html",
    # Verified Southeast LA customer consent: static no-JS fallback (2026-10-24).
    "long-beach-appliance-pickup": "long-beach-appliance-pickup/index.html",
    "bellflower-appliance-pickup": "bellflower-appliance-pickup/index.html",
    "compton-appliance-pickup": "compton-appliance-pickup/index.html",
    "south-gate-appliance-pickup": "south-gate-appliance-pickup/index.html",
    # Verified coastal Orange County static quote consent gaps (2026-10-24).
    "huntington-beach-appliance-pickup": "huntington-beach-appliance-pickup/index.html",
    "costa-mesa-appliance-pickup": "costa-mesa-appliance-pickup/index.html",
    "newport-beach-appliance-pickup": "newport-beach-appliance-pickup/index.html",
    "laguna-niguel-appliance-pickup": "laguna-niguel-appliance-pickup/index.html",
    # Verified SGV and OC customer no-JS quote choices (2026-10-24).
    "san-marino-appliance-pickup": "san-marino-appliance-pickup/index.html",
    "sierra-madre-appliance-pickup": "sierra-madre-appliance-pickup/index.html",
    "buena-park-appliance-pickup": "buena-park-appliance-pickup/index.html",
    "yorba-linda-appliance-pickup": "yorba-linda-appliance-pickup/index.html",
    "mission-viejo-appliance-pickup": "mission-viejo-appliance-pickup/index.html",
    # Upland / Ontario / Montclair specialty request consent and attribution (2026-10-24).
    "upland-washer-dryer-pickup": "upland-washer-dryer-pickup/index.html",
    # Existing IE specialty pages: preserve lead city and optional quote without JS.
    "upland-freezer-pickup": "upland-freezer-pickup/index.html",
    "upland-stove-oven-pickup": "upland-stove-oven-pickup/index.html",
    "corona-washer-dryer-pickup": "corona-washer-dryer-pickup/index.html",
    "upland-refrigerator-pickup": "upland-refrigerator-pickup/index.html",
    "ontario-washer-dryer-pickup": "ontario-washer-dryer-pickup/index.html",
    "montclair-washer-dryer-pickup": "montclair-washer-dryer-pickup/index.html",
    # Source-confirmed California specialty no-JS paid quote gaps (2026-10-24).
    "riverside-washer-dryer-pickup": "riverside-washer-dryer-pickup/index.html",
    "riverside-refrigerator-pickup": "riverside-refrigerator-pickup/index.html",
    "anaheim-washer-dryer-pickup": "anaheim-washer-dryer-pickup/index.html",
    "pomona-washer-dryer-pickup": "pomona-washer-dryer-pickup/index.html",
    # Six confirmed CA laundry leads needing no-JS city/service and consent safety (2026-10-24).
    "la-habra-washer-dryer-pickup": "la-habra-washer-dryer-pickup/index.html",
    "whittier-washer-dryer-pickup": "whittier-washer-dryer-pickup/index.html",
    "montebello-washer-dryer-pickup": "montebello-washer-dryer-pickup/index.html",
    "garden-grove-washer-dryer-pickup": "garden-grove-washer-dryer-pickup/index.html",
    "orange-washer-dryer-pickup": "orange-washer-dryer-pickup/index.html",
    "buena-park-washer-dryer-pickup": "buena-park-washer-dryer-pickup/index.html",
    # Verified OC laundry source, mobile and optional quote fallback (2026-10-24).
    "chino-hills-washer-dryer-pickup": "chino-hills-washer-dryer-pickup/index.html",
    # Verified Inland Empire laundry form truth and no-JS quote fallback.
    "chino-washer-dryer-pickup": "chino-washer-dryer-pickup/index.html",
    "rialto-washer-dryer-pickup": "rialto-washer-dryer-pickup/index.html",
    "huntington-beach-washer-dryer-pickup": "huntington-beach-washer-dryer-pickup/index.html",
    "irvine-washer-dryer-pickup": "irvine-washer-dryer-pickup/index.html",
    "tustin-washer-dryer-pickup": "tustin-washer-dryer-pickup/index.html",
    "fullerton-washer-dryer-pickup": "fullerton-washer-dryer-pickup/index.html",
    "brea-washer-dryer-pickup": "brea-washer-dryer-pickup/index.html",
    "yorba-linda-washer-dryer-pickup": "yorba-linda-washer-dryer-pickup/index.html",
    "lake-forest-washer-dryer-pickup": "lake-forest-washer-dryer-pickup/index.html",
    "mission-viejo-washer-dryer-pickup": "mission-viejo-washer-dryer-pickup/index.html",
    "laguna-niguel-washer-dryer-pickup": "laguna-niguel-washer-dryer-pickup/index.html",
    "san-clemente-washer-dryer-pickup": "san-clemente-washer-dryer-pickup/index.html",
    # Verified Rosemead/Temple City/Monterey Park/El Monte laundry consent (2026-10-24).
    "rosemead-washer-dryer-pickup": "rosemead-washer-dryer-pickup/index.html",
    "santa-ana-washer-dryer-pickup": "santa-ana-washer-dryer-pickup/index.html",
    "temple-city-washer-dryer-pickup": "temple-city-washer-dryer-pickup/index.html",
    "monterey-park-washer-dryer-pickup": "monterey-park-washer-dryer-pickup/index.html",
    "el-monte-washer-dryer-pickup": "el-monte-washer-dryer-pickup/index.html",
    # Verified additional SGV laundry no-JS paid quote consent (2026-10-24).
    "monrovia-washer-dryer-pickup": "monrovia-washer-dryer-pickup/index.html",
    "duarte-washer-dryer-pickup": "duarte-washer-dryer-pickup/index.html",
    "covina-washer-dryer-pickup": "covina-washer-dryer-pickup/index.html",
    "san-gabriel-washer-dryer-pickup": "san-gabriel-washer-dryer-pickup/index.html",
    "west-covina-washer-dryer-pickup": "west-covina-washer-dryer-pickup/index.html",
    # Verified Arcadia/Glendora laundry static consent and attribution (2026-10-24).
    "arcadia-washer-dryer-pickup": "arcadia-washer-dryer-pickup/index.html",
    "glendora-washer-dryer-pickup": "glendora-washer-dryer-pickup/index.html",
    # Verified Pasadena/Alhambra/La Puente/Baldwin Park laundry no-JS quote consent (2026-10-24).
    "alhambra-washer-dryer-pickup": "alhambra-washer-dryer-pickup/index.html",
    "pasadena-washer-dryer-pickup": "pasadena-washer-dryer-pickup/index.html",
    "la-puente-washer-dryer-pickup": "la-puente-washer-dryer-pickup/index.html",
    "baldwin-park-washer-dryer-pickup": "baldwin-park-washer-dryer-pickup/index.html",
    # Existing SGV/Pomona Valley specialty request forms: optional customer quote consent (2026-10-24).
    "pasadena-refrigerator-pickup": "pasadena-refrigerator-pickup/index.html",
    "claremont-washer-dryer-pickup": "claremont-washer-dryer-pickup/index.html",
    "san-dimas-washer-dryer-pickup": "san-dimas-washer-dryer-pickup/index.html",
    "la-verne-washer-dryer-pickup": "la-verne-washer-dryer-pickup/index.html",
    # Existing CA laundry request forms: optional quote and complete routing (2026-10-25).
    "san-bernardino-washer-dryer-pickup": "san-bernardino-washer-dryer-pickup/index.html",
    "moreno-valley-washer-dryer-pickup": "moreno-valley-washer-dryer-pickup/index.html",
    "downey-washer-dryer-pickup": "downey-washer-dryer-pickup/index.html",
    # Fontana specialty request forms: verified no-JS optional quote selection (2026-10-24).
    "fontana-stove-oven-pickup": "fontana-stove-oven-pickup/index.html",
    "fontana-refrigerator-pickup": "fontana-refrigerator-pickup/index.html",
    "fontana-freezer-pickup": "fontana-freezer-pickup/index.html",
    "fontana-washer-dryer-pickup": "fontana-washer-dryer-pickup/index.html",
}
# Existing Los Angeles appliance-category forms use descriptive source-page attribution.
# Validate the no-JavaScript quote choice without changing the source identifiers.
# Protect two existing SGV city forms: optional quote, explicit customer input,
# truthful city attribution and usable phone/ZIP mobile hints.
SGV_FOOTHILL_GENERAL_INTAKE = {
    "la-canada-flintridge-appliance-pickup": "La Cañada Flintridge",
    "south-pasadena-appliance-pickup": "South Pasadena",
}

# Keep legacy High Desert/Antelope city forms honest and reliable with no-JS quote consent.
HIGH_DESERT_ANTELOPE_GENERAL = {
    "victorville-appliance-pickup": "Victorville",
    "hesperia-appliance-pickup": "Hesperia",
    "adelanto-appliance-pickup": "Adelanto",
    "apple-valley-appliance-pickup": "Apple Valley",
    "palmdale-appliance-pickup": "Palmdale",
    "lancaster-appliance-pickup": "Lancaster",
}

# Coachella Valley no-JavaScript customer contact and consent safeguards.
COACHELLA_GENERAL_INTAKE = {
    "palm-springs-appliance-pickup": "Palm Springs",
    "palm-desert-appliance-pickup": "Palm Desert",
    "la-quinta-appliance-pickup": "La Quinta",
    "rancho-mirage-appliance-pickup": "Rancho Mirage",
}

LA_SPECIALTY_SOURCE = {
    "los-angeles-refrigerator-pickup": "Los Angeles refrigerator page",
    "los-angeles-freezer-pickup": "Los Angeles freezer page",
    "los-angeles-stove-oven-pickup": "Los Angeles stove oven page",
}
# Regress the three existing Los Angeles appliance specialty forms' no-JS
# service attribution without changing historical source_page labels.
LA_SPECIALTY_SERVICE = {
    "los-angeles-refrigerator-pickup": "Refrigerator pickup",
    "los-angeles-freezer-pickup": "Freezer pickup",
    "los-angeles-stove-oven-pickup": "Stove, range and oven pickup",
}
# Three verified Inland Empire specialty intake/source gaps from 2026-10-24.
IE_SPECIALTY_INTAKE = {
    "corona-washer-dryer-pickup": ("Corona", "Washer and dryer pickup"),
    "upland-freezer-pickup": ("Upland", "Freezer pickup"),
    "upland-stove-oven-pickup": ("Upland", "Stove, range and oven pickup"),
}
# City/service attribution, required condition and mobile hints for three existing CA forms.
# San Bernardino city is a required visible input; other two keep a hidden city.
NEXT_WAVE_LAUNDRY_INTAKE = {
    "san-bernardino-washer-dryer-pickup": "San Bernardino",
    "moreno-valley-washer-dryer-pickup": "Moreno Valley",
    "downey-washer-dryer-pickup": "Downey",
    "fresno-washer-dryer-pickup": "Fresno",
}
# Source-only city/service, required-choice and mobile contract for five IE laundry forms.
IE_FIVE_LAUNDRY_INTAKE = {
    "highland-washer-dryer-pickup": "Highland",
    "redlands-washer-dryer-pickup": "Redlands",
    "eastvale-washer-dryer-pickup": "Eastvale",
    "colton-washer-dryer-pickup": "Colton",
    "jurupa-valley-washer-dryer-pickup": "Jurupa Valley",
}
# Source-only intake contract for six existing Southern California laundry forms.
SOCAL_LAUNDRY_INTAKE = {
    "la-habra-washer-dryer-pickup": "La Habra",
    "whittier-washer-dryer-pickup": "Whittier",
    "montebello-washer-dryer-pickup": "Montebello",
    "garden-grove-washer-dryer-pickup": "Garden Grove",
    "orange-washer-dryer-pickup": "Orange",
    "buena-park-washer-dryer-pickup": "Buena Park",
}
# Three existing SGV laundry forms must retain city and service in no-JS posts.
SGV_LAUNDRY_INTAKE = {
    "temple-city-washer-dryer-pickup": "Temple City",
    "monterey-park-washer-dryer-pickup": "Monterey Park",
    "el-monte-washer-dryer-pickup": "El Monte",
}
OC_LAUNDRY_INTAKE = {
    "chino-hills-washer-dryer-pickup": "Chino Hills",
    "huntington-beach-washer-dryer-pickup": "Huntington Beach",
    "irvine-washer-dryer-pickup": "Irvine",
    "tustin-washer-dryer-pickup": "Tustin",
    "fullerton-washer-dryer-pickup": "Fullerton",
    "brea-washer-dryer-pickup": "Brea",
    "yorba-linda-washer-dryer-pickup": "Yorba Linda",
    "lake-forest-washer-dryer-pickup": "Lake Forest",
    "mission-viejo-washer-dryer-pickup": "Mission Viejo",
    "laguna-niguel-washer-dryer-pickup": "Laguna Niguel",
    "san-clemente-washer-dryer-pickup": "San Clemente",
}
# Preserve truthful condition and legacy no-JS service attribution on three Foothill laundry forms.
FOOTHILL_LAUNDRY_INTAKE = {
    "fontana-washer-dryer-pickup": "Fontana",
    "upland-washer-dryer-pickup": "Upland",
    "claremont-washer-dryer-pickup": "Claremont",
}
# Protect six verified San Gabriel Valley/Pomona Valley laundry form choices and attribution.
SGV_SIX_LAUNDRY_INTAKE = {
    "pasadena-washer-dryer-pickup": "Pasadena",
    "arcadia-washer-dryer-pickup": "Arcadia",
    "san-gabriel-washer-dryer-pickup": "San Gabriel",
    "glendora-washer-dryer-pickup": "Glendora",
    "la-verne-washer-dryer-pickup": "La Verne",
    "san-dimas-washer-dryer-pickup": "San Dimas",
}

# Five priority countywide forms: preserve free-first consent and truthful attribution.
CA_FIVE_COUNTY_INTAKE = {
    "los-angeles-county-appliance-pickup",
    "orange-county-appliance-pickup",
    "riverside-county-appliance-pickup",
    "san-bernardino-county-appliance-pickup",
    "san-diego-county-appliance-pickup",
}

# Protect truthful condition and no-JS service attribution on three existing CA laundry forms.
CA_LAUNDRY_WORKING_ISSUES = {
    "riverside-washer-dryer-pickup": "Riverside",
    "ontario-washer-dryer-pickup": "Ontario",
    "anaheim-washer-dryer-pickup": "Anaheim",
    "los-angeles-washer-dryer-pickup": "Los Angeles",
    "pomona-washer-dryer-pickup": "Pomona",
    "santa-ana-washer-dryer-pickup": "Santa Ana",
    "monrovia-washer-dryer-pickup": "Monrovia",
    "west-covina-washer-dryer-pickup": "West Covina",
    "duarte-washer-dryer-pickup": "Duarte",
}
# Preserve honest nondefault conditions, city/service routing, and mobile fields
# for existing Chino, Chino Hills and Rialto laundry request forms.
IE_THREE_LAUNDRY_TRUTH = {
    "chino-washer-dryer-pickup": "Chino",
    "chino-hills-washer-dryer-pickup": "Chino Hills",
    "rialto-washer-dryer-pickup": "Rialto",
}
# Five existing Orange County laundry request forms: preserve truthful condition and routing.
OC_FIVE_LAUNDRY_TRUTH = {
    "garden-grove-washer-dryer-pickup": "Garden Grove",
    "fullerton-washer-dryer-pickup": "Fullerton",
    "brea-washer-dryer-pickup": "Brea",
    "huntington-beach-washer-dryer-pickup": "Huntington Beach",
    "buena-park-washer-dryer-pickup": "Buena Park",
}
# Same owner-approved fallback on four existing Oregon request forms.
OREGON_PAGES = {
    "portland-appliance-pickup": "portland-appliance-pickup/index.html",
    "salem-appliance-pickup": "salem-appliance-pickup/index.html",
    "portland-washer-dryer-pickup": "portland-washer-dryer-pickup/index.html",
    "salem-washer-dryer-pickup": "salem-washer-dryer-pickup/index.html",
}
ENDPOINT = "https://formspree.io/f/mvzeapzd"

class Forms(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms = []
        self.active = None
    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == "form":
            self.active = {"attrs": attrs, "inputs": [], "selects": []}
            self.forms.append(self.active)
        elif self.active is not None:
            if tag == "input": self.active["inputs"].append(attrs)
            if tag == "select": self.active["selects"].append({"attrs": attrs, "options": [], "option_attrs": []})
            if tag == "option" and self.active["selects"]:
                self.active["selects"][-1]["options"].append(attrs.get("value"))
                self.active["selects"][-1]["option_attrs"].append(attrs)
    def handle_endtag(self, tag):
        if tag == "form": self.active = None

def inspect(label, html, expected_source=None):
    parser = Forms(); parser.feed(html)
    problems = []
    forms = [f for f in parser.forms if f["attrs"].get("action") == ENDPOINT]
    if len(forms) != 1:
        return [f"{label}: expected exactly one approved Formspree form, got {len(forms)}"]
    form = forms[0]
    if form["attrs"].get("method", "").lower() != "post": problems.append(f"{label}: must POST")
    inputs = form["inputs"]
    if len([a for a in inputs if a.get("name") == "source_page" and a.get("value") == (expected_source or label)]) != 1:
        problems.append(f"{label}: missing source_page attribution")
    if len([a for a in inputs if a.get("name") == "phone" and a.get("type") == "tel" and "required" in a]) != 1:
        problems.append(f"{label}: required telephone missing")
    choices = [s for s in form["selects"] if s["attrs"].get("name") == "paid_removal_preference"]
    if len(choices) != 1:
        problems.append(f"{label}: expected one static optional paid quote selector")
    else:
        s = choices[0]
        if "required" in s["attrs"]: problems.append(f"{label}: paid quote selector must be optional")
        if s["options"] != ["", "free_only", "quote_ok"]:
            problems.append(f"{label}: default / free-only / quote-only consent values changed")
        if any("selected" in a for a in s["option_attrs"][1:]):
            problems.append(f"{label}: paid quote or free-only must not be preselected")
    if label in COACHELLA_GENERAL_INTAKE:
        expected_city = COACHELLA_GENERAL_INTAKE[label]
        for field, expected in (("city", expected_city), ("state", "California"), ("service", "General major appliance pickup")):
            matches = [a for a in inputs if a.get("name") == field and a.get("type") == "hidden" and a.get("value") == expected]
            if len(matches) != 1:
                problems.append(f"{label}: missing or incorrect static {field} label")
        for field, mode, auto in (("phone", "tel", "tel"), ("zip", "numeric", "postal-code")):
            matches = [a for a in inputs if a.get("name") == field]
            if len(matches) != 1 or "required" not in matches[0] or matches[0].get("inputmode") != mode or matches[0].get("autocomplete") != auto:
                problems.append(f"{label}: required mobile {field} hints missing")
        for field in ("appliance", "condition"):
            matches = [a for a in form["selects"] if a["attrs"].get("name") == field]
            if len(matches) != 1 or "required" not in matches[0]["attrs"] or not matches[0]["options"] or matches[0]["options"][0] != "":
                problems.append(f"{label}: {field} requires explicit customer choice")
            elif any("selected" in a for a in matches[0]["option_attrs"][1:]):
                problems.append(f"{label}: {field} silently preselects an appliance/condition")
    # Customer forms on three county hubs must not silently lose city,
    # service attribution, phone, optional paid quote or appliance truth.
    if label in CA_FIVE_COUNTY_INTAKE:
        for name, value in (("state", "California"), ("service", "General major appliance pickup")):
            matches = [a for a in inputs if a.get("name") == name and a.get("type") == "hidden" and a.get("value") == value]
            if len(matches) != 1:
                problems.append(f"{label}: missing or incorrect static {name} attribution")
        cities = [a for a in inputs if a.get("name") == "city"]
        if len(cities) != 1 or "required" not in cities[0] or cities[0].get("type") == "hidden" or cities[0].get("value"):
            problems.append(f"{label}: customer must enter actual pickup city")
        for name, mode, auto in (("phone", "tel", "tel"), ("zip", "numeric", "postal-code")):
            matches = [a for a in inputs if a.get("name") == name]
            if len(matches) != 1 or "required" not in matches[0] or matches[0].get("inputmode") != mode or matches[0].get("autocomplete") != auto:
                problems.append(f"{label}: mobile {name} input contract changed")
            elif name == "phone" and matches[0].get("type") != "tel":
                problems.append(f"{label}: telephone type must stay tel")
        for name in ("appliance", "condition"):
            matches = [a for a in form["selects"] if a["attrs"].get("name") == name]
            if len(matches) != 1 or "required" not in matches[0]["attrs"] or not matches[0]["options"] or matches[0]["options"][0] != "":
                problems.append(f"{label}: {name} must require explicit selection")
            elif any("selected" in a for a in matches[0]["option_attrs"][1:]):
                problems.append(f"{label}: {name} cannot be preselected")
            elif name == "condition" and matches[0]["options"].count("Working With Issues") != 1:
                problems.append(f"{label}: working-with-issues option missing or duplicated")
    if label in HIGH_DESERT_ANTELOPE_GENERAL:
        expected_city = HIGH_DESERT_ANTELOPE_GENERAL[label]
        for key, expected in (("city", expected_city), ("state", "California"), ("service", "General major appliance pickup")):
            found = [a for a in inputs if a.get("name") == key and a.get("value") == expected]
            if len(found) != 1 or (key != "city" and found[0].get("type") != "hidden"):
                problems.append(f"{label}: missing or incorrect static {key} attribution")
        for key, mode, auto in (("phone", "tel", "tel"), ("zip", "numeric", "postal-code")):
            found = [a for a in inputs if a.get("name") == key]
            if len(found) != 1 or "required" not in found[0] or found[0].get("inputmode") != mode or found[0].get("autocomplete") != auto:
                problems.append(f"{label}: required mobile {key} field changed")
        conditions = [x for x in form["selects"] if x["attrs"].get("name") == "condition"]
        if len(conditions) != 1 or "required" not in conditions[0]["attrs"] or not conditions[0]["options"] or conditions[0]["options"][0] != "":
            problems.append(f"{label}: customer must explicitly choose condition")
        elif any("selected" in a for a in conditions[0]["option_attrs"][1:]):
            problems.append(f"{label}: condition must not preselect a working answer")
    if label in SGV_FOOTHILL_GENERAL_INTAKE:
        expected_city = SGV_FOOTHILL_GENERAL_INTAKE[label]
        for field, expected in (("city", expected_city), ("state", "California"), ("service", "General major appliance pickup")):
            hits = [a for a in inputs if a.get("name") == field and a.get("value") == expected]
            if len(hits) != 1 or (field != "city" and hits[0].get("type") != "hidden"):
                problems.append(f"{label}: incorrect static {field} attribution")
        for field, mode, auto in (("phone", "tel", "tel"), ("zip", "numeric", "postal-code")):
            hits = [a for a in inputs if a.get("name") == field]
            if len(hits) != 1 or "required" not in hits[0] or hits[0].get("inputmode") != mode or hits[0].get("autocomplete") != auto:
                problems.append(f"{label}: incorrect required mobile {field} input")
        for field in ("appliance", "condition"):
            candidates = [entry for entry in form["selects"] if entry["attrs"].get("name") == field]
            if len(candidates) != 1 or "required" not in candidates[0]["attrs"] or not candidates[0]["options"] or candidates[0]["options"][0] != "":
                problems.append(f"{label}: {field} must require explicit choice")
            elif any("selected" in option for option in candidates[0]["option_attrs"][1:]):
                problems.append(f"{label}: must not preselect {field}")
    if label in LA_SPECIALTY_SERVICE:
        expected_service = LA_SPECIALTY_SERVICE[label]
        service_inputs = [a for a in inputs if a.get("name") == "service"]
        if len(service_inputs) != 1 or service_inputs[0].get("type") != "hidden" or service_inputs[0].get("value") != expected_service:
            problems.append(f"{label}: missing or incorrect static service attribution")
        if len([a for a in inputs if a.get("name") == "city" and a.get("value") == "Los Angeles"]) != 1:
            problems.append(f"{label}: incorrect Los Angeles city attribution")
        if len([a for a in inputs if a.get("name") == "state" and a.get("value") == "California"]) != 1:
            problems.append(f"{label}: incorrect California state attribution")
    # A running machine with a known issue is not necessarily fully working or broken.
    # Keep the truthful nondefault condition and service tag on these existing forms.
    if label in CA_LAUNDRY_WORKING_ISSUES:
        expected_city = CA_LAUNDRY_WORKING_ISSUES[label]
        for field, expected in (("state", "California"), ("service", "Washer and dryer pickup")):
            matches = [a for a in inputs if a.get("name") == field and a.get("type") == "hidden" and a.get("value") == expected]
            if len(matches) != 1:
                problems.append(f"{label}: missing or incorrect static {field} attribution")
        cities = [a for a in inputs if a.get("name") == "city" and a.get("value") == expected_city and "required" in a]
        if len(cities) != 1:
            problems.append(f"{label}: required city attribution changed")
        for field, mode, auto in (("phone", "tel", "tel"), ("zip", "numeric", "postal-code")):
            matches = [a for a in inputs if a.get("name") == field]
            if len(matches) != 1 or "required" not in matches[0] or matches[0].get("inputmode") != mode or matches[0].get("autocomplete") != auto:
                problems.append(f"{label}: required mobile {field} input changed")
        for field in ("appliance", "condition"):
            matches = [a for a in form["selects"] if a["attrs"].get("name") == field]
            if len(matches) != 1 or "required" not in matches[0]["attrs"] or not matches[0]["options"] or matches[0]["options"][0] != "":
                problems.append(f"{label}: {field} must require an explicit choice")
            elif any("selected" in attrs for attrs in matches[0]["option_attrs"][1:]):
                problems.append(f"{label}: {field} must not preselect a condition or appliance")
            elif field == "condition" and matches[0]["options"].count("Working With Issues") != 1:
                problems.append(f"{label}: working-with-issues choice missing or duplicated")
    # Existing Foothill laundry forms must distinguish working-with-issues,
    # retain their original service tag, and provide usable mobile input.
    if label in FOOTHILL_LAUNDRY_INTAKE:
        expected_city = FOOTHILL_LAUNDRY_INTAKE[label]
        for field, expected in (("state", "California"), ("service", "Washer Dryer Pickup")):
            matches = [a for a in inputs if a.get("name") == field and a.get("type") == "hidden" and a.get("value") == expected]
            if len(matches) != 1:
                problems.append(f"{label}: missing or incorrect static {field} attribution")
        cities = [a for a in inputs if a.get("name") == "city" and a.get("value") == expected_city and "required" in a]
        if len(cities) != 1:
            problems.append(f"{label}: required city attribution changed")
        for field, mode, auto in (("phone", "tel", "tel"), ("zip", "numeric", "postal-code")):
            matches = [a for a in inputs if a.get("name") == field]
            if len(matches) != 1 or "required" not in matches[0] or matches[0].get("inputmode") != mode or matches[0].get("autocomplete") != auto:
                problems.append(f"{label}: required mobile {field} input changed")
        for field in ("appliance", "condition"):
            matches = [a for a in form["selects"] if a["attrs"].get("name") == field]
            if len(matches) != 1 or "required" not in matches[0]["attrs"] or not matches[0]["options"] or matches[0]["options"][0] != "":
                problems.append(f"{label}: {field} must require an explicit choice")
            elif any("selected" in attrs for attrs in matches[0]["option_attrs"][1:]):
                problems.append(f"{label}: {field} must not preselect an appliance/condition")
            elif field == "condition" and matches[0]["options"].count("Working With Issues") != 1:
                problems.append(f"{label}: working-with-issues choice missing or duplicated")
    # Verified SGV/Pomona Valley laundry forms: truthfully report a running
    # machine with a known issue, while preserving no-JS city/service routing.
    if label in SGV_SIX_LAUNDRY_INTAKE:
        expected_city = SGV_SIX_LAUNDRY_INTAKE[label]
        for field, expected in (("state", "California"), ("service", "Washer and dryer pickup")):
            matches = [a for a in inputs if a.get("name") == field and a.get("type") == "hidden" and a.get("value") == expected]
            if len(matches) != 1:
                problems.append(f"{label}: missing or incorrect static {field} attribution")
        cities = [a for a in inputs if a.get("name") == "city" and a.get("value") == expected_city and "required" in a]
        if len(cities) != 1:
            problems.append(f"{label}: required city attribution changed")
        for field, mode, auto in (("phone", "tel", "tel"), ("zip", "numeric", "postal-code")):
            matches = [a for a in inputs if a.get("name") == field]
            if len(matches) != 1 or "required" not in matches[0] or matches[0].get("inputmode") != mode or matches[0].get("autocomplete") != auto:
                problems.append(f"{label}: required mobile {field} input changed")
        for field in ("appliance", "condition"):
            matches = [a for a in form["selects"] if a["attrs"].get("name") == field]
            if len(matches) != 1 or "required" not in matches[0]["attrs"] or not matches[0]["options"] or matches[0]["options"][0] != "":
                problems.append(f"{label}: {field} must require an explicit choice")
            elif any("selected" in attrs for attrs in matches[0]["option_attrs"][1:]):
                problems.append(f"{label}: {field} must not preselect an appliance/condition")
            elif field == "condition" and matches[0]["options"].count("Working With Issues") != 1:
                problems.append(f"{label}: working-with-issues choice missing or duplicated")
    if label in IE_THREE_LAUNDRY_TRUTH:
        expected_city = IE_THREE_LAUNDRY_TRUTH[label]
        for field, expected in (("state", "California"), ("service", "Washer and dryer pickup")):
            hits = [a for a in inputs if a.get("name") == field and a.get("type") == "hidden" and a.get("value") == expected]
            if len(hits) != 1:
                problems.append(f"{label}: missing or incorrect static {field} attribution")
        cities = [a for a in inputs if a.get("name") == "city" and a.get("value") == expected_city]
        if len(cities) != 1 or (cities[0].get("type") != "hidden" and "required" not in cities[0]):
            problems.append(f"{label}: incorrect pickup city attribution")
        for field, mode, auto in (("phone", "tel", "tel"), ("zip", "numeric", "postal-code")):
            hits = [a for a in inputs if a.get("name") == field]
            if len(hits) != 1 or "required" not in hits[0] or hits[0].get("inputmode") != mode or hits[0].get("autocomplete") != auto:
                problems.append(f"{label}: required mobile {field} hints missing")
        for field in ("appliance", "condition"):
            choices = [a for a in form["selects"] if a["attrs"].get("name") == field]
            if len(choices) != 1 or "required" not in choices[0]["attrs"] or not choices[0]["options"] or choices[0]["options"][0] != "":
                problems.append(f"{label}: {field} must require an explicit choice")
            elif any("selected" in a for a in choices[0]["option_attrs"][1:]):
                problems.append(f"{label}: {field} cannot silently preselect a value")
            elif field == "condition" and choices[0]["options"].count("Working With Issues") != 1:
                problems.append(f"{label}: truthful running-with-issues option missing or duplicated")
    # Accurate running-with-issues condition and no-JS intake on existing OC forms.
    if label in OC_FIVE_LAUNDRY_TRUTH:
        expected_city = OC_FIVE_LAUNDRY_TRUTH[label]
        services = [a for a in inputs if a.get("name") == "service" and a.get("type") == "hidden" and a.get("value") == "Washer and dryer pickup"]
        if len(services) != 1:
            problems.append(f"{label}: laundry service attribution changed")
        for field, expected in (("city", expected_city), ("state", "California")):
            matches = [a for a in inputs if a.get("name") == field and a.get("value") == expected]
            if len(matches) != 1 or (matches[0].get("type") != "hidden" and "required" not in matches[0]):
                problems.append(f"{label}: incorrect {field} attribution")
        for field, mode, auto in (("phone", "tel", "tel"), ("zip", "numeric", "postal-code")):
            matches = [a for a in inputs if a.get("name") == field]
            if len(matches) != 1 or "required" not in matches[0] or matches[0].get("inputmode") != mode or matches[0].get("autocomplete") != auto:
                problems.append(f"{label}: mobile {field} hints missing")
        for field in ("appliance", "condition"):
            matches = [a for a in form["selects"] if a["attrs"].get("name") == field]
            if len(matches) != 1 or "required" not in matches[0]["attrs"] or not matches[0]["options"] or matches[0]["options"][0] != "":
                problems.append(f"{label}: {field} requires explicit customer selection")
            elif any("selected" in attrs for attrs in matches[0]["option_attrs"][1:]):
                problems.append(f"{label}: {field} cannot preselect a nonempty option")
            elif field == "condition" and matches[0]["options"].count("Working With Issues") != 1:
                problems.append(f"{label}: running-with-issues condition missing or duplicated")
    # Oregon laundry customers need a truthful explicit option for a machine
    # that runs but has a known issue; do not preselect any condition.
    if label in ("portland-washer-dryer-pickup", "salem-washer-dryer-pickup"):
        conditions = [a for a in form["selects"] if a["attrs"].get("name") == "condition"]
        if len(conditions) != 1 or "required" not in conditions[0]["attrs"] or not conditions[0]["options"] or conditions[0]["options"][0] != "":
            problems.append(f"{label}: condition must require explicit choice")
        elif "Working With Issues" not in conditions[0]["options"] or any("selected" in a for a in conditions[0]["option_attrs"][1:]):
            problems.append(f"{label}: working-with-issues choice missing or condition preselected")
    if label in IE_SPECIALTY_INTAKE:
        expected_city, expected_service = IE_SPECIALTY_INTAKE[label]
        for key, expected in (("city", expected_city), ("state", "California"), ("service", expected_service)):
            matches = [a for a in inputs if a.get("name") == key and a.get("type") == "hidden" and a.get("value") == expected]
            if len(matches) != 1:
                problems.append(f"{label}: incorrect static {key} attribution")
        if label == "corona-washer-dryer-pickup":
            phone = [a for a in inputs if a.get("name") == "phone"]
            zip_inputs = [a for a in inputs if a.get("name") == "zip"]
            if len(phone) != 1 or phone[0].get("autocomplete") != "tel" or phone[0].get("inputmode") != "tel":
                problems.append(f"{label}: mobile phone hints missing")
            if len(zip_inputs) != 1 or zip_inputs[0].get("autocomplete") != "postal-code" or zip_inputs[0].get("inputmode") != "numeric":
                problems.append(f"{label}: mobile ZIP hints missing")
    if label in NEXT_WAVE_LAUNDRY_INTAKE:
        expected_city = NEXT_WAVE_LAUNDRY_INTAKE[label]
        for key, expected in (("city", expected_city), ("state", "California"), ("service", "Washer and dryer pickup")):
            matches = [a for a in inputs if a.get("name") == key and a.get("value") == expected]
            if len(matches) != 1 or (key != "city" and matches[0].get("type") != "hidden"):
                problems.append(f"{label}: missing or incorrect {key} attribution")
        for key, required_mode, auto in (("phone", "tel", "tel"), ("zip", "numeric", "postal-code")):
            matches = [a for a in inputs if a.get("name") == key]
            if len(matches) != 1 or "required" not in matches[0] or matches[0].get("inputmode") != required_mode or matches[0].get("autocomplete") != auto:
                problems.append(f"{label}: missing required mobile {key} input")
        for key in ("condition", "appliance"):
            matches = [x for x in form["selects"] if x["attrs"].get("name") == key]
            if len(matches) != 1 or "required" not in matches[0]["attrs"] or matches[0]["options"][0] != "":
                problems.append(f"{label}: {key} must require explicit customer choice")
            elif any("selected" in item for item in matches[0]["option_attrs"][1:]):
                problems.append(f"{label}: {key} must not preselect an appliance/condition")
    if label in IE_FIVE_LAUNDRY_INTAKE:
        expected_city = IE_FIVE_LAUNDRY_INTAKE[label]
        for field, expected in (("city", expected_city), ("state", "California"), ("service", "Washer and dryer pickup")):
            hits = [a for a in inputs if a.get("name") == field and a.get("value") == expected]
            if len(hits) != 1 or (field != "city" and hits[0].get("type") != "hidden"):
                problems.append(f"{label}: missing or incorrect {field} attribution")
        for field, mode, auto in (("phone", "tel", "tel"), ("zip", "numeric", "postal-code")):
            hits = [a for a in inputs if a.get("name") == field]
            if len(hits) != 1 or "required" not in hits[0] or hits[0].get("inputmode") != mode or hits[0].get("autocomplete") != auto:
                problems.append(f"{label}: incomplete required mobile {field} field")
        for field in ("appliance", "condition"):
            choices = [s for s in form["selects"] if s["attrs"].get("name") == field]
            if len(choices) != 1 or "required" not in choices[0]["attrs"] or not choices[0]["options"] or choices[0]["options"][0] != "":
                problems.append(f"{label}: {field} must require explicit selection")
            elif any("selected" in item for item in choices[0]["option_attrs"][1:]):
                problems.append(f"{label}: {field} must not preselect an unverified answer")
    if label in SOCAL_LAUNDRY_INTAKE:
        expected_city = SOCAL_LAUNDRY_INTAKE[label]
        for field, expected in (("city", expected_city), ("state", "California"), ("service", "Washer and dryer pickup")):
            hits = [a for a in inputs if a.get("name") == field and a.get("type") == "hidden" and a.get("value") == expected]
            if len(hits) != 1:
                problems.append(f"{label}: static {field} attribution incorrect or absent")
        for field in ("phone", "zip"):
            hits = [a for a in inputs if a.get("name") == field]
            expected_mode = "tel" if field == "phone" else "numeric"
            expected_auto = "tel" if field == "phone" else "postal-code"
            if len(hits) != 1 or hits[0].get("inputmode") != expected_mode or hits[0].get("autocomplete") != expected_auto or "required" not in hits[0]:
                problems.append(f"{label}: incomplete required mobile {field} input")
        if label in ("la-habra-washer-dryer-pickup", "whittier-washer-dryer-pickup", "montebello-washer-dryer-pickup"):
            matching = [s for s in form["selects"] if s["attrs"].get("name") == "appliance"]
            if len(matching) != 1 or "required" not in matching[0]["attrs"] or not matching[0]["options"] or matching[0]["options"][0] != "":
                problems.append(f"{label}: appliance requires explicit selection")
            elif any("selected" in option for option in matching[0]["option_attrs"][1:]):
                problems.append(f"{label}: appliance must not be preselected")
    if label in SGV_LAUNDRY_INTAKE:
        expected_city = SGV_LAUNDRY_INTAKE[label]
        for field, expected in (("city", expected_city), ("state", "California"), ("service", "Washer and dryer pickup")):
            matched = [a for a in inputs if a.get("name") == field and a.get("type") == "hidden" and a.get("value") == expected]
            if len(matched) != 1:
                problems.append(f"{label}: missing or incorrect static {field}")
        if label == "monterey-park-washer-dryer-pickup":
            for field in ("condition", "appliance"):
                matching = [entry for entry in form["selects"] if entry["attrs"].get("name") == field]
                if len(matching) != 1 or "required" not in matching[0]["attrs"] or not matching[0]["options"] or matching[0]["options"][0] != "":
                    problems.append(f"{label}: {field} requires blank initial option and customer selection")
                elif any("selected" in a for a in matching[0]["option_attrs"][1:]):
                    problems.append(f"{label}: {field} preselects an unverified answer")
    if label in OC_LAUNDRY_INTAKE:
        expected_city = OC_LAUNDRY_INTAKE[label]
        for key, expected in (("city", expected_city), ("state", "California")):
            matches = [a for a in inputs if a.get("name") == key and a.get("value") == expected]
            if len(matches) != 1:
                problems.append(f"{label}: missing or incorrect static {key} attribution")
        services = [a for a in inputs if a.get("name") == "service"]
        if len(services) != 1 or "washer" not in services[0].get("value", "").lower() or "dryer" not in services[0].get("value", "").lower():
            problems.append(f"{label}: missing or incorrect laundry service attribution")
        for key in ("condition", "appliance"):
            matching = [entry for entry in form["selects"] if entry["attrs"].get("name") == key]
            if len(matching) != 1 or "required" not in matching[0]["attrs"] or not matching[0]["options"] or matching[0]["options"][0] != "":
                problems.append(f"{label}: {key} requires explicit customer selection")
            elif any("selected" in a for a in matching[0]["option_attrs"][1:]):
                problems.append(f"{label}: {key} preselects an unverified answer")
    # Verified lead-condition safety: never silently default to "Fully Working".
    if label in ("rosemead-washer-dryer-pickup", "santa-ana-washer-dryer-pickup"):
        if len([a for a in inputs if a.get("name") == "service" and a.get("value") == "Washer and dryer pickup" and a.get("type") == "hidden"]) != 1:
            problems.append(f"{label}: static laundry service tag missing")
        if label == "rosemead-washer-dryer-pickup":
            if len([a for a in inputs if a.get("name") == "city" and a.get("value") == "Rosemead" and a.get("type") == "hidden"]) != 1:
                problems.append(f"{label}: static city tag missing")
            for field in ("condition", "appliance"):
                group = [s for s in form["selects"] if s["attrs"].get("name") == field]
                if len(group) != 1 or "required" not in group[0]["attrs"] or not group[0]["options"] or group[0]["options"][0] != "":
                    problems.append(f"{label}: {field} must require explicit customer selection")
                elif any("selected" in a for a in group[0]["option_attrs"][1:]):
                    problems.append(f"{label}: {field} must not preselect working condition/appliance")
        if label == "santa-ana-washer-dryer-pickup":
            if len([a for a in inputs if a.get("name") == "city" and a.get("value") == "Santa Ana" and "required" in a]) != 1:
                problems.append(f"{label}: required city must default to Santa Ana")
    # Two LA County washer/dryer pages must submit complete city/service
    # attribution even when customer-routing.js fails or is disabled.
    if label in ("san-fernando-washer-dryer-pickup", "los-angeles-washer-dryer-pickup"):
        expected_city = "San Fernando" if label.startswith("san-fernando") else "Los Angeles"
        city_inputs = [a for a in inputs if a.get("name") == "city"]
        if len(city_inputs) != 1 or not ("required" in city_inputs[0] or city_inputs[0].get("type") == "hidden"):
            problems.append(f"{label}: city must be present in static form")
        elif city_inputs[0].get("value") != expected_city:
            problems.append(f"{label}: wrong city attribution {city_inputs[0].get('value')}")
        if len([a for a in inputs if a.get("name") == "service" and a.get("value") == "Washer and dryer pickup"]) != 1:
            problems.append(f"{label}: static laundry service attribution absent")
        phones = [a for a in inputs if a.get("name") == "phone"]
        if len(phones) != 1 or phones[0].get("autocomplete") != "tel" or phones[0].get("inputmode") != "tel":
            problems.append(f"{label}: mobile telephone hints missing")
        zips = [a for a in inputs if a.get("name") == "zip"]
        if len(zips) != 1 or zips[0].get("inputmode") != "numeric" or zips[0].get("autocomplete") != "postal-code":
            problems.append(f"{label}: postal-code mobile hints missing")
    return problems

def fixture_checks():
    label = "san-fernando-valley-appliance-pickup"
    good = (
        f'<form action="{ENDPOINT}" method="POST">'
        f'<input type="hidden" name="source_page" value="{label}">'
        '<input name="phone" type="tel" required>'
        '<select name="paid_removal_preference">'
        '<option value=""></option><option value="free_only"></option>'
        '<option value="quote_ok"></option></select></form>'
    )
    assert inspect(label, good) == [], "valid optional quote preference rejected"
    unsafe = (
        good.replace('<option value=""></option>', '<option value="quote_ok"></option>'),
        good.replace('<select name="paid_removal_preference">', '<select required name="paid_removal_preference">'),
        good.replace('name="paid_removal_preference"', 'name="unknown"'),
        good.replace('type="tel" required', 'type="tel"'),
        good.replace('name="source_page"', 'name="other_page"'),
        good.replace(ENDPOINT, "https://example.org/unauthorized"),
        good.replace('<option value="quote_ok"></option>', '<option value="quote_ok" selected></option>'),
    )
    for tampered in unsafe:
        assert inspect(label, tampered), "unsafe fixture went undetected"
    # Five countywide request forms: positive fixture plus intentional regressions.
    for county_label in sorted(CA_FIVE_COUNTY_INTAKE):
        county_good = (
            f'<form action="{ENDPOINT}" method="POST">'
            f'<input type="hidden" name="source_page" value="{county_label}">'
            '<input type="hidden" name="state" value="California">'
            '<input type="hidden" name="service" value="General major appliance pickup">'
            '<input type="text" name="city" required>'
            '<input type="tel" name="phone" required autocomplete="tel" inputmode="tel">'
            '<input name="zip" required autocomplete="postal-code" inputmode="numeric">'
            '<select name="appliance" required><option value=""></option><option>Washer</option></select>'
            '<select name="condition" required><option value=""></option><option>Fully Working</option>'
            '<option value="Working With Issues"></option><option>Needs Repair</option></select>'
            '<select name="paid_removal_preference"><option value=""></option>'
            '<option value="free_only"></option><option value="quote_ok"></option></select></form>'
        )
        assert not inspect(county_label, county_good), f"valid county intake rejected: {county_label}"
        for old, new in (
            ('name="service"', 'name="lost_service"'),
            ('name="source_page"', 'name="lost_source"'),
            ('name="city" required', 'name="city"'),
            ('type="text" name="city"', 'type="hidden" name="city"'),
            ('value="Working With Issues"', 'value="Needs Repair"'),
            ('name="condition" required', 'name="condition"'),
            ('inputmode="numeric"', 'inputmode="text"'),
            ('autocomplete="tel"', 'autocomplete="off"'),
            ('name="paid_removal_preference"', 'name="no_paid_quote"'),
        ):
            assert inspect(county_label, county_good.replace(old, new)), f"county intake defect not caught: {county_label}: {old}"
    # Five existing OC laundry forms: verify valid and tampered no-JS source.
    for oc_label, oc_city in OC_FIVE_LAUNDRY_TRUTH.items():
        oc_good = (
            f'<form action="{ENDPOINT}" method="POST">'
            f'<input type="hidden" name="source_page" value="{oc_label}">'
            f'<input type="hidden" name="city" value="{oc_city}">'
            '<input type="hidden" name="state" value="California">'
            '<input type="hidden" name="service" value="Washer and dryer pickup">'
            '<input type="tel" name="phone" required autocomplete="tel" inputmode="tel">'
            '<input name="zip" required autocomplete="postal-code" inputmode="numeric">'
            '<select name="appliance" required><option value=""></option><option>Washer</option></select>'
            '<select name="condition" required><option value=""></option><option>Fully Working</option>'
            '<option value="Working With Issues"></option><option>Needs Repair</option></select>'
            '<select name="paid_removal_preference"><option value=""></option>'
            '<option value="free_only"></option><option value="quote_ok"></option></select></form>'
        )
        assert not inspect(oc_label, oc_good), f"valid OC laundry form rejected: {oc_label}"
        for before, after in (
            ('name="source_page"', 'name="wrong_source"'),
            ('name="city"', 'name="wrong_city"'),
            ('name="service"', 'name="wrong_service"'),
            ('value="California"', 'value="Oregon"'),
            ('inputmode="numeric"', 'inputmode="text"'),
            ('autocomplete="tel"', 'autocomplete="off"'),
            ('name="appliance" required', 'name="appliance"'),
            ('name="condition" required', 'name="condition"'),
            ('value="Working With Issues"', 'value="Fully Working"'),
            ('name="paid_removal_preference"', 'name="unknown_consent"'),
        ):
            assert inspect(oc_label, oc_good.replace(before, after)), f"OC laundry defect missed: {oc_label}: {before}"
        # Huntington Beach has editable city/state; this must also remain valid.
        if oc_label == "huntington-beach-washer-dryer-pickup":
            editable = oc_good.replace('type="hidden" name="city"', 'name="city" required').replace('type="hidden" name="state"', 'name="state" required')
            assert not inspect(oc_label, editable), "editable OC city/state incorrectly rejected"
    # Source-only positive/negative regression for three verified IE laundry fixes.
    for ie_label, ie_city in IE_THREE_LAUNDRY_TRUTH.items():
        ie_good = (
            f'<form action="{ENDPOINT}" method="POST">'
            f'<input type="hidden" name="source_page" value="{ie_label}">'
            f'<input type="hidden" name="city" value="{ie_city}">'
            '<input type="hidden" name="state" value="California">'
            '<input type="hidden" name="service" value="Washer and dryer pickup">'
            '<input type="tel" name="phone" required autocomplete="tel" inputmode="tel">'
            '<input name="zip" required autocomplete="postal-code" inputmode="numeric">'
            '<select name="appliance" required><option value=""></option><option>Washer</option></select>'
            '<select name="condition" required><option value=""></option><option>Fully Working</option>'
            '<option value="Working With Issues"></option><option>Needs Repair</option></select>'
            '<select name="paid_removal_preference"><option value=""></option>'
            '<option value="free_only"></option><option value="quote_ok"></option></select></form>'
        )
        assert not inspect(ie_label, ie_good), f"valid IE laundry form rejected: {ie_label}"
        for old, new in (
            ('name="source_page"', 'name="lost_source"'),
            (f'value="{ie_city}"', 'value="Other City"'),
            ('name="service"', 'name="lost_service"'),
            ('inputmode="tel"', 'inputmode="numeric"'),
            ('autocomplete="postal-code"', 'autocomplete="off"'),
            ('<option value=""></option><option>Washer', '<option>Washer'),
            ('name="condition" required', 'name="condition"'),
            ('value="Working With Issues"', 'value="Needs Repair"'),
            ('<option value="Working With Issues"></option>', '<option value="Working With Issues" selected></option>'),
            ('name="paid_removal_preference"', 'name="no_consent"'),
        ):
            assert inspect(ie_label, ie_good.replace(old, new)), f"IE laundry defect not caught: {ie_label}: {old}"
    # California laundry source/condition regression, including negative fixtures.
    ca_label = "riverside-washer-dryer-pickup"
    ca_good = (
        f'<form action="{ENDPOINT}" method="POST">'
        f'<input type="hidden" name="source_page" value="{ca_label}">'
        '<input type="hidden" name="state" value="California">'
        '<input type="hidden" name="service" value="Washer and dryer pickup">'
        '<input name="city" value="Riverside" required>'
        '<input name="phone" type="tel" required autocomplete="tel" inputmode="tel">'
        '<input name="zip" required autocomplete="postal-code" inputmode="numeric">'
        '<select name="appliance" required><option value=""></option><option>Washer</option></select>'
        '<select name="condition" required><option value=""></option><option>Fully Working</option>'
        '<option value="Working With Issues"></option><option>Needs Repair</option></select>'
        '<select name="paid_removal_preference"><option value=""></option>'
        '<option value="free_only"></option><option value="quote_ok"></option></select></form>'
    )
    for city in CA_LAUNDRY_WORKING_ISSUES.values():
        ca_case_label = city.lower().replace(" ", "-") + "-washer-dryer-pickup"
        example = ca_good.replace(ca_label, ca_case_label).replace('value="Riverside"', f'value="{city}"')
        assert not inspect(ca_case_label, example), f"valid California laundry fixture rejected: {city}"
        for old, new in (
            ('value="Working With Issues"', 'value="Needs Repair"'),
            ('name="service"', 'name="lost_service"'),
            ('name="condition" required', 'name="condition"'),
            ('name="appliance" required', 'name="appliance"'),
            ('autocomplete="tel"', 'autocomplete="off"'),
            ('inputmode="numeric"', 'inputmode="text"'),
        ):
            assert inspect(ca_case_label, example.replace(old, new)), f"California laundry defect not caught: {city}: {old}"
    for old, new in (
        ('name="service"', 'name="other_service"'),
        ('value="Riverside"', 'value="Other City"'),
        ('value="Working With Issues"', 'value="Fully Working"'),
        ('<option value="Working With Issues"></option>', '<option value="Working With Issues" selected></option>'),
        ('name="condition" required', 'name="condition"'),
        ('inputmode="numeric"', 'inputmode="text"'),
    ):
        assert inspect(ca_label, ca_good.replace(old, new)), f"CA laundry defect undetected: {old}"
    # Foothill city laundry intake: keep legacy service attribution, truthful condition and mobile inputs.
    for foothill_label, foothill_city in FOOTHILL_LAUNDRY_INTAKE.items():
        foothill_good = (
            f'<form action="{ENDPOINT}" method="POST">'
            f'<input type="hidden" name="source_page" value="{foothill_label}">'
            '<input type="hidden" name="state" value="California">'
            '<input type="hidden" name="service" value="Washer Dryer Pickup">'
            f'<input name="city" value="{foothill_city}" required>'
            '<input type="tel" name="phone" required autocomplete="tel" inputmode="tel">'
            '<input name="zip" required autocomplete="postal-code" inputmode="numeric">'
            '<select name="appliance" required><option value=""></option><option>Washer</option></select>'
            '<select name="condition" required><option value=""></option><option>Fully Working</option>'
            '<option value="Working With Issues"></option><option>Needs Repair</option></select>'
            '<select name="paid_removal_preference"><option value=""></option>'
            '<option value="free_only"></option><option value="quote_ok"></option></select></form>'
        )
        assert not inspect(foothill_label, foothill_good), f"valid Foothill laundry fixture rejected: {foothill_city}"
        for old, new in (
            ('name="service"', 'name="other_service"'),
            (f'value="{foothill_city}"', 'value="Other City"'),
            ('value="Working With Issues"', 'value="Fully Working"'),
            ('<option value="Working With Issues"></option>', '<option value="Working With Issues" selected></option>'),
            ('name="condition" required', 'name="condition"'),
            ('inputmode="numeric"', 'inputmode="text"'),
        ):
            assert inspect(foothill_label, foothill_good.replace(old, new)), f"Foothill laundry defect undetected: {old}"
    # Regression fixtures for all six verified SGV/Pomona Valley intake repairs.
    for sgv_label, sgv_city in SGV_SIX_LAUNDRY_INTAKE.items():
        sgv_good = (
            f'<form action="{ENDPOINT}" method="POST">'
            f'<input type="hidden" name="source_page" value="{sgv_label}">'
            '<input type="hidden" name="state" value="California">'
            '<input type="hidden" name="service" value="Washer and dryer pickup">'
            f'<input name="city" value="{sgv_city}" required>'
            '<input type="tel" name="phone" required autocomplete="tel" inputmode="tel">'
            '<input name="zip" required autocomplete="postal-code" inputmode="numeric">'
            '<select name="appliance" required><option value=""></option><option>Washer</option></select>'
            '<select name="condition" required><option value=""></option><option>Fully Working</option>'
            '<option value="Working With Issues"></option><option>Needs Repair</option></select>'
            '<select name="paid_removal_preference"><option value=""></option>'
            '<option value="free_only"></option><option value="quote_ok"></option></select></form>'
        )
        assert not inspect(sgv_label, sgv_good), f"valid SGV laundry fixture rejected: {sgv_city}"
        for old, new in (
            ('name="service"', 'name="untracked_service"'),
            (f'value="{sgv_city}"', 'value="Other City"'),
            ('value="Working With Issues"', 'value="Fully Working"'),
            ('<option value="Working With Issues"></option>', '<option value="Working With Issues" selected></option>'),
            ('name="condition" required', 'name="condition"'),
            ('autocomplete="postal-code"', 'autocomplete="off"'),
            ('name="paid_removal_preference"', 'name="consent_missing"'),
        ):
            assert inspect(sgv_label, sgv_good.replace(old, new)), f"SGV laundry regression not caught: {sgv_city}: {old}"
    # Coachella Valley working-condition and paid-quote consent must remain explicit.
    valley_label = "la-quinta-appliance-pickup"
    valley_good = (
        f'<form action="{ENDPOINT}" method="POST">'
        f'<input type="hidden" name="source_page" value="{valley_label}">'
        '<input type="hidden" name="state" value="California">'
        '<input type="hidden" name="city" value="La Quinta">'
        '<input type="hidden" name="service" value="General major appliance pickup">'
        '<input type="tel" name="phone" required autocomplete="tel" inputmode="tel">'
        '<input name="zip" required autocomplete="postal-code" inputmode="numeric">'
        '<select name="appliance" required><option value=""></option><option>Washer</option></select>'
        '<select name="condition" required><option value=""></option><option>Fully Working</option></select>'
        '<select name="paid_removal_preference"><option value=""></option>'
        '<option value="free_only"></option><option value="quote_ok"></option></select></form>'
    )
    assert not inspect(valley_label, valley_good), "valid La Quinta intake rejected"
    for old, new in (
        ('value="La Quinta"', 'value="Palm Springs"'),
        ('name="service"', 'name="wrong_service"'),
        ('name="paid_removal_preference"', 'name="missing_consent"'),
        ('inputmode="numeric"', 'inputmode="text"'),
        ('name="condition" required', 'name="condition"'),
        ('<option value=""></option><option>Washer', '<option>Washer'),
    ):
        assert inspect(valley_label, valley_good.replace(old, new)), f"Coachella intake regression undetected: {old}"
    # High Desert + Antelope Valley: explicit no-JS city, service and quote safeguards.
    desert_label = "palmdale-appliance-pickup"
    desert_good = (
        f'<form action="{ENDPOINT}" method="POST">'
        f'<input type="hidden" name="source_page" value="{desert_label}">'
        '<input type="hidden" name="state" value="California">'
        '<input type="hidden" name="service" value="General major appliance pickup">'
        '<input name="city" value="Palmdale" required>'
        '<input type="tel" name="phone" required autocomplete="tel" inputmode="tel">'
        '<input name="zip" required inputmode="numeric" autocomplete="postal-code">'
        '<select name="condition" required><option value=""></option><option>Needs Repair</option></select>'
        '<select name="paid_removal_preference"><option value=""></option>'
        '<option value="free_only"></option><option value="quote_ok"></option></select></form>'
    )
    assert not inspect(desert_label, desert_good), "valid Palmdale quote consent rejected"
    for old, new in (
        ('value="Palmdale"', 'value="Lancaster"'),
        ('name="service"', 'name="no_service"'),
        ('name="paid_removal_preference"', 'name="missing_opt_in"'),
        ('inputmode="tel"', 'inputmode="numeric"'),
        ('autocomplete="postal-code"', 'autocomplete="off"'),
        ('name="condition" required', 'name="condition"'),
        ('<option value=""></option><option>Needs', '<option>Needs'),
    ):
        assert inspect(desert_label, desert_good.replace(old, new)), f"Desert/Antelope customer regression undetected: {old}"
    # California general city intake: positive and negative no-JS quote/attribution checks.
    foothill_label = "south-pasadena-appliance-pickup"
    foothill_good = (
        f'<form action="{ENDPOINT}" method="POST">'
        f'<input type="hidden" name="source_page" value="{foothill_label}">'
        '<input type="hidden" name="state" value="California">'
        '<input type="hidden" name="service" value="General major appliance pickup">'
        '<input name="city" value="South Pasadena" required>'
        '<input name="phone" type="tel" required autocomplete="tel" inputmode="tel">'
        '<input name="zip" required autocomplete="postal-code" inputmode="numeric">'
        '<select name="appliance" required><option value=""></option><option>Washer</option></select>'
        '<select name="condition" required><option value=""></option><option>Fully Working</option></select>'
        '<select name="paid_removal_preference"><option value=""></option>'
        '<option value="free_only"></option><option value="quote_ok"></option></select></form>'
    )
    assert not inspect(foothill_label, foothill_good), "valid South Pasadena customer intake rejected"
    for old, new in (
        ('value="South Pasadena"', 'value="Pasadena"'),
        ('name="service"', 'name="wrong_service"'),
        ('name="paid_removal_preference"', 'name="missing_quote_choice"'),
        ('autocomplete="tel"', 'autocomplete="off"'),
        ('name="condition" required', 'name="condition"'),
        ('<option value=""></option><option>Washer', '<option>Washer'),
    ):
        assert inspect(foothill_label, foothill_good.replace(old, new)), f"South Pasadena regression undetected: {old}"
    # Oregon laundry positive and negative truthful-condition fixtures.
    oregon_label = "portland-washer-dryer-pickup"
    oregon_good = good.replace(f'value="{label}"', f'value="{oregon_label}"').replace(
        '</select></form>',
        '</select><select name="condition" required><option value=""></option>'
        '<option value="Working With Issues"></option></select></form>'
    )
    assert not inspect(oregon_label, oregon_good), "valid Oregon laundry condition rejected"
    for old, new in (
        ('value="Working With Issues"', 'value="Unknown Condition"'),
        ('name="condition" required', 'name="condition"'),
        ('<option value="Working With Issues"></option>', '<option value="Working With Issues" selected></option>'),
    ):
        assert inspect(oregon_label, oregon_good.replace(old, new)), f"Oregon condition regression not caught: {old}"
    # Source-only condition, attribution and consent fixture for legacy
    # LA County forms with an implicit "Washer" first choice.
    la_label = "montebello-washer-dryer-pickup"
    la_good = good.replace(f'value="{label}"', f'value="{la_label}"').replace(
        '<input name="phone" type="tel" required>',
        '<input name="phone" type="tel" required autocomplete="tel" inputmode="tel">'
        '<input type="hidden" name="city" value="Montebello">'
        '<input type="hidden" name="state" value="California">'
        '<input type="hidden" name="service" value="Washer and dryer pickup">'
        '<input name="zip" required inputmode="numeric" autocomplete="postal-code">'
        '<select name="appliance" required><option value=""></option><option>Washer</option></select>'
    )
    assert not inspect(la_label, la_good), "valid legacy CA laundry intake rejected"
    assert inspect(la_label, la_good.replace('value="Montebello"', 'value="Pomona"')), "wrong city must fail"
    assert inspect(la_label, la_good.replace('name="appliance" required', 'name="appliance"')), "appliance default must fail"
    assert inspect(la_label, la_good.replace('name="service"', 'name="other_service"')), "missing service must fail"
    # A missing, wrong-city or wrong-service form must be rejected offline.
    sgv_label = "monterey-park-washer-dryer-pickup"
    sgv_good = good.replace(f'value="{label}"', f'value="{sgv_label}"').replace(
        '<input name="phone" type="tel" required>',
        '<input name="phone" type="tel" required>'
        '<input type="hidden" name="city" value="Monterey Park">'
        '<input type="hidden" name="state" value="California">'
        '<input type="hidden" name="service" value="Washer and dryer pickup">'
        '<select name="condition" required><option value=""></option><option value="Fully Working"></option></select>'
        '<select name="appliance" required><option value=""></option><option value="Washer"></option></select>'
    )
    assert not inspect(sgv_label, sgv_good), "SGV valid form should pass"
    assert inspect(sgv_label, sgv_good.replace('value="Monterey Park"', 'value="Pasadena"')), "wrong SGV city not caught"
    assert inspect(sgv_label, sgv_good.replace('name="condition" required', 'name="condition"')), "missing required condition not caught"
    assert inspect(sgv_label, sgv_good.replace('<option value=""></option><option value="Fully Working"', '<option value="Fully Working"></option><option value=""')), "preselected working condition not caught"
    # Positive/negative static fixtures for the 2026-10-25 customer-intake batch.
    new_label = "moreno-valley-washer-dryer-pickup"
    new_good = (
        f'<form action="{ENDPOINT}" method="POST">'
        f'<input type="hidden" name="source_page" value="{new_label}">'
        '<input type="hidden" name="city" value="Moreno Valley">'
        '<input type="hidden" name="state" value="California">'
        '<input type="hidden" name="service" value="Washer and dryer pickup">'
        '<input type="tel" name="phone" required autocomplete="tel" inputmode="tel">'
        '<input name="zip" required autocomplete="postal-code" inputmode="numeric">'
        '<select name="appliance" required><option value=""></option><option>Washer</option></select>'
        '<select name="condition" required><option value=""></option><option>Fully Working</option></select>'
        '<select name="paid_removal_preference"><option value=""></option>'
        '<option value="free_only"></option><option value="quote_ok"></option></select>'
        '</form>'
    )
    assert not inspect(new_label, new_good), "valid new CA laundry form rejected"
    for old, new in (
        ('value="Moreno Valley"', 'value="Fontana"'),
        ('name="service"', 'name="untracked_service"'),
        ('inputmode="tel"', 'inputmode="numeric"'),
        ('name="paid_removal_preference"', 'name="no_consent"'),
        ('name="condition" required', 'name="condition"'),
    ):
        assert inspect(new_label, new_good.replace(old, new)), f"new CA laundry defect undetected: {old}"
    # Fresno-specific positive/negative no-JS intake regression cases.
    fresno_label = "fresno-washer-dryer-pickup"
    fresno_good = new_good.replace('value="moreno-valley-washer-dryer-pickup"',
        'value="fresno-washer-dryer-pickup"').replace('value="Moreno Valley"', 'value="Fresno"')
    assert not inspect(fresno_label, fresno_good), "valid Fresno specialty form rejected"
    for old, new in (
        ('value="Fresno"', 'value="Clovis"'),
        ('name="service"', 'name="service_missing"'),
        ('name="paid_removal_preference"', 'name="no_consent"'),
        ('name="condition" required', 'name="condition"'),
        ('inputmode="numeric"', 'inputmode="text"'),
    ):
        assert inspect(fresno_label, fresno_good.replace(old, new)), f"Fresno intake defect undetected: {old}"
    # IE five-form intake: positive and negative static consent/attribution fixtures.
    ie_label = "eastvale-washer-dryer-pickup"
    ie_good = (
        f'<form action="{ENDPOINT}" method="POST">'
        f'<input type="hidden" name="source_page" value="{ie_label}">'
        '<input type="hidden" name="city" value="Eastvale">'
        '<input type="hidden" name="state" value="California">'
        '<input type="hidden" name="service" value="Washer and dryer pickup">'
        '<input name="phone" type="tel" required autocomplete="tel" inputmode="tel">'
        '<input name="zip" required autocomplete="postal-code" inputmode="numeric">'
        '<select name="appliance" required><option value=""></option><option>Washer</option></select>'
        '<select name="condition" required><option value=""></option><option>Fully Working</option></select>'
        '<select name="paid_removal_preference"><option value=""></option>'
        '<option value="free_only"></option><option value="quote_ok"></option></select></form>'
    )
    assert not inspect(ie_label, ie_good), "valid IE five-form fixture rejected"
    for old, new in (
        ('value="Eastvale"', 'value="Fontana"'),
        ('value="Washer and dryer pickup"', 'value="General appliance pickup"'),
        ('inputmode="tel"', 'inputmode="numeric"'),
        ('autocomplete="postal-code"', 'autocomplete="off"'),
        ('name="paid_removal_preference"', 'name="consent_missing"'),
        ('name="condition" required', 'name="condition"'),
        ('<option value=""></option><option>Washer', '<option>Washer'),
    ):
        assert inspect(ie_label, ie_good.replace(old, new)), f"IE intake regression not caught: {old}"
    # Prevent regression of a real no-JavaScript Inland Empire city/service gap.
    ie_good = good.replace(f'value="{label}"', 'value="upland-freezer-pickup"').replace(
        '<input name="phone" type="tel" required>',
        '<input name="phone" type="tel" required><input name="city" type="hidden" value="Upland"><input name="state" type="hidden" value="California"><input name="service" type="hidden" value="Freezer pickup">'
    )
    assert not inspect("upland-freezer-pickup", ie_good), "valid Upland static fields rejected"
    assert inspect("upland-freezer-pickup", ie_good.replace('value="Upland"', 'value="Fontana"')), "wrong city allowed"
    assert inspect("upland-freezer-pickup", ie_good.replace('value="Freezer pickup"', 'value="Washer pickup"')), "wrong service allowed"
    special = good.replace(
        f'<input type="hidden" name="source_page" value="{label}">',
        '<input type="hidden" name="source_page" value="Los Angeles refrigerator page">'
        '<input type="hidden" name="city" value="Los Angeles">'
        '<input type="hidden" name="state" value="California">'
        '<input type="hidden" name="service" value="Refrigerator pickup">'
    )
    assert not inspect("los-angeles-refrigerator-pickup", special, "Los Angeles refrigerator page")
    assert inspect("los-angeles-refrigerator-pickup", special, "wrong attribution")
    assert inspect("los-angeles-refrigerator-pickup", special.replace('value="Refrigerator pickup"', 'value="Freezer pickup"'), "Los Angeles refrigerator page")


if __name__ == "__main__":
    fixture_checks()
    errors = []
    for label, path in {**PAGES, **OREGON_PAGES}.items():
        errors.extend(inspect(label, Path(path).read_text(encoding="utf-8")))
    for label, source in LA_SPECIALTY_SOURCE.items():
        path = Path(label) / "index.html"
        errors.extend(inspect(label, path.read_text(encoding="utf-8"), source))
    # Guard against silently accepting automatic paid consent.
    first = Path(next(iter(PAGES.values()))).read_text(encoding="utf-8")
    assert "quote_ok" in first and 'value=""' in first
    print(f"SFV_STATIC_PAID_QUOTE_PAGES {len(PAGES)}")
    print(f"CALIFORNIA_STATIC_PAID_QUOTE_PAGES {len(PAGES)}")
    print(f"OREGON_STATIC_PAID_QUOTE_PAGES {len(OREGON_PAGES)}")
    print(f"LA_SPECIALTY_STATIC_PAID_QUOTE_PAGES {len(LA_SPECIALTY_SOURCE)}")
    print(f"TOTAL_STATIC_PAID_QUOTE_PAGES {len(PAGES) + len(OREGON_PAGES) + len(LA_SPECIALTY_SOURCE)}")
    print(f"SFV_STATIC_PAID_QUOTE_ERRORS {len(errors)}")
    for error in errors: print("FAIL:", error)
    raise SystemExit(1 if errors else 0)
