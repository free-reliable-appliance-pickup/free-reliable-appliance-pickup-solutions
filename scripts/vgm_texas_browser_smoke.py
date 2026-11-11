#!/usr/bin/env python3
"""Browser-only Texas draft checks; synthetic intercepted POSTs never leave CI."""
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ("/houston-appliance-pickup/", "Houston", "Houston Metro"),
    ("/dallas-washer-dryer-pickup/", "Dallas", "Dallas-Fort Worth"),
    ("/austin-refrigerator-pickup/", "Austin", "Austin Metro"),
    ("/san-antonio-freezer-pickup/", "San Antonio", "San Antonio Metro"),
    ("/el-paso-stove-oven-pickup/", "El Paso", "El Paso Metro"),
    ("/kingwood-tx-freezer-pickup/", "Houston", "Houston Metro"),
    ("/watauga-tx-appliance-pickup/", "Watauga", "Dallas-Fort Worth"),
]
VIEWPORTS = [
    ("desktop", {"width": 1365, "height": 900}),
    ("mobile", {"width": 390, "height": 844}),
]


class QuietHandler(SimpleHTTPRequestHandler):
    """Serve checked-out pages without logging requests or touching production."""

    def log_message(self, *_args):
        pass

    def send_head(self):
        """Reject raw, URL-encoded, and symlinked checkout Git-metadata paths."""
        target = Path(self.translate_path(self.path))
        # translate_path applies the same URL decoding used by the file server.
        if any(part.casefold() == ".git" for part in target.parts) or any(
            part.casefold() == ".git" for part in target.resolve(strict=False).parts
        ):
            self.send_error(404)
            return None
        return super().send_head()



def check_statewide_hub(browser, base, preview_dir):
    """Verify the statewide form is genuinely first in rendered mobile/desktop DOM."""
    for mode, viewport in VIEWPORTS:
        context = browser.new_context(viewport=viewport)
        page = context.new_page()
        try:
            page.route("https://formspree.io/**", lambda route: route.abort())
            response = page.goto(
                base + "/texas-appliance-pickup/",
                wait_until="domcontentloaded",
                timeout=30000,
            )
            if not response or response.status != 200:
                raise AssertionError("Texas statewide hub not HTTP 200")
            page.wait_for_function(
                "() => !!window.FreeReliableCustomerRouting && "
                "!!document.querySelector('#request .site-request-next-steps')",
                timeout=15000,
            )
            if page.locator("main > section").first.get_attribute("id") != "request":
                raise AssertionError("Texas statewide request is not the first main section")
            form = page.locator('#request form[action="https://formspree.io/f/mvzeapzd"]')
            if form.count() != 1:
                raise AssertionError("Texas statewide request form missing or duplicated")
            for name in ("name", "phone", "address", "city", "zip", "appliance",
                         "condition", "floor", "stairs", "photos_available"):
                control = form.locator('[name="' + name + '"]')
                if control.count() != 1 or control.get_attribute("required") is None:
                    raise AssertionError("Texas statewide required field: " + name)
            if page.locator("#request .site-photo-first-intake").count():
                raise AssertionError("Photo instructions were inserted ahead of statewide inputs")
            steps = page.locator("#request > .site-request-next-steps")
            if steps.count() != 1:
                raise AssertionError("Statewide next steps missing or duplicated")
            steps_after_form = steps.evaluate(
                "(node) => Boolean(node.previousElementSibling && "
                "node.previousElementSibling.tagName === 'FORM')"
            )
            if not steps_after_form:
                raise AssertionError("Statewide next-step cards appear before form fields")
            if preview_dir:
                page.screenshot(
                    path=str(preview_dir / (mode + "-texas-statewide-form-first.png")),
                    full_page=False,
                    animations="disabled",
                )
            page.locator("#texas-quick-city").fill("Katy")
            page.locator("#texas-quick-continue").click()
            if form.locator('[name="city"]').input_value() != "Katy":
                raise AssertionError("Texas city shortcut failed to populate main form")
            print("PASS", mode, "Texas statewide real form first; city shortcut fills city")
        finally:
            context.close()

def run():
    """Check rendered draft images, form selectors, route labels and quote consent."""
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        partial(QuietHandler, directory=str(ROOT)),
    )
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = "http://127.0.0.1:" + str(server.server_port)
    failures = []
    passed = 0
    # The preview is a CI artifact only: never publish screenshots or capture
    # synthetic/customer form values. Keep output outside the served checkout.
    preview_root = os.environ.get("VGM_TEXAS_SCREENSHOT_DIR", "").strip()
    preview_dir = Path(preview_root).resolve() if preview_root else None
    if preview_dir:
        if preview_dir == ROOT or ROOT in preview_dir.parents:
            raise SystemExit("Screenshot output must be outside served checkout")
        preview_dir.mkdir(parents=True, exist_ok=True)
    try:
        # Test the HTTP boundary, not just the Python path-guard function.
        # Both URL forms must be rejected before page scripts can read .git.
        from urllib.error import HTTPError
        from urllib.request import urlopen

        for protected_path in ("/.git/config", "/%2egit/config"):
            try:
                with urlopen(base + protected_path, timeout=5) as response:
                    status = response.status
            except HTTPError as error:
                status = error.code
            if status != 404:
                raise AssertionError(
                    "Git metadata accessible via " + protected_path + ": HTTP " + str(status)
                )
        print("PASS Git metadata denied for direct and URL-encoded access")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                check_statewide_hub(browser, base, preview_dir)
                for mode, viewport in VIEWPORTS:
                    context = browser.new_context(viewport=viewport)
                    try:
                        for path, city, region in CASES:
                            page = context.new_page()
                            label = mode + " " + path
                            try:
                                # Refuse any accidental live POST, including scripts.
                                page.route("https://formspree.io/**", lambda route: route.abort())
                                response = page.goto(base + path, wait_until="domcontentloaded", timeout=30000)
                                if not response or response.status != 200:
                                    raise AssertionError("draft page not HTTP 200")
                                page.locator("h1").first.wait_for(state="visible")
                                robots = page.locator('meta[name="robots"]').get_attribute("content") or ""
                                if "noindex" not in robots.lower():
                                    raise AssertionError("unapproved Texas page lost noindex")
                                if page.locator("#request").count() != 1:
                                    raise AssertionError("missing or duplicated #request anchor")
                                form = page.locator('form[action="https://formspree.io/f/mvzeapzd"]')
                                if form.count() != 1:
                                    raise AssertionError("missing or duplicate Formspree form")
                                if (form.get_attribute("method") or "").lower() != "post":
                                    raise AssertionError("wrong form method")
                                if form.locator('[name="state"]').input_value() != "TX":
                                    raise AssertionError("incorrect state")
                                if form.locator('[name="source_page"]').input_value() != path.strip("/"):
                                    raise AssertionError("source attribution does not match page")
                                for name in ("name", "phone", "address", "city", "zip",
                                             "appliance", "condition", "floor", "stairs",
                                             "photos_available"):
                                    control = form.locator('[name="' + name + '"]')
                                    if control.count() != 1 or control.get_attribute("required") is None:
                                        raise AssertionError("missing required " + name)
                                if form.locator('[name="zip"]').get_attribute("pattern") != "[0-9]{5}":
                                    raise AssertionError("five-digit ZIP validation missing")
                                photos = page.locator("img").evaluate_all(
                                    """(images) => images.filter(img => !/logo|brand|icon/i.test(
                                    img.getAttribute('src') || '')).map(img => img.getAttribute('src'))"""
                                )
                                if len(photos) != 1:
                                    raise AssertionError("expected one appliance photo, found " + str(len(photos)))
                                hero = page.locator('img[src="' + photos[0] + '"]')
                                hero.scroll_into_view_if_needed()
                                width = hero.evaluate(
                                    "(img) => img.decode().then(() => img.naturalWidth).catch(() => 0)"
                                )
                                if width < 100:
                                    raise AssertionError("appliance photo did not decode")
                                # Capture visible page layout before populating ANY
                                # form control, including synthetic browser-only data.
                                if preview_dir:
                                    safe_name = path.strip("/").replace("/", "-")
                                    page.screenshot(
                                        path=str(preview_dir / (mode + "-" + safe_name + ".png")),
                                        full_page=True,
                                        animations="disabled",
                                    )
                                page.wait_for_function(
                                    "() => !!(window.FreeReliableCustomerRouting && "
                                    "document.querySelector('form[action*=formspree] select[name=paid_option], "
                                    "form[action*=formspree] select[name=paid_removal_preference]'))",
                                    timeout=15000,
                                )
                                city_control = form.locator('[name="city"]')
                                city_control.fill(city)
                                page.evaluate("() => window.FreeReliableCustomerRouting.load()")
                                choice = form.locator('select[name="paid_option"],select[name="paid_removal_preference"]')
                                if choice.count() != 1:
                                    raise AssertionError("duplicated or missing visible quote preference")
                                legacy = choice.get_attribute("name") == "paid_option"
                                options = ([
                                    ("Yes, after seeing the price", "QUOTE_REVIEW_ONLY", "quote_ok"),
                                    ("No, free pickup only", "FREE_PICKUP_ONLY", "free_only"),
                                    ("", "NO_PAID_QUOTE_AUTHORIZATION", ""),
                                ] if legacy else [
                                    ("quote_ok", "QUOTE_REVIEW_ONLY", "quote_ok"),
                                    ("free_only", "FREE_PICKUP_ONLY", "free_only"),
                                    ("", "NO_PAID_QUOTE_AUTHORIZATION", ""),
                                ])
                                for value, expected, normalized in options:
                                    choice.select_option(value)
                                    result = page.evaluate("""() => {
                                        const form = document.querySelector('form[action*="formspree.io"]');
                                        window.FreeReliableCustomerRouting.qualify(form);
                                        const value = name => form.querySelector('[name="' + name + '"]')?.value || '';
                                        return {
                                            quote: value('Paid Removal Quote Gate'),
                                            normalized: value('paid_removal_preference'),
                                            region: value('Routing Region'),
                                            status: value('Routing Market Status'),
                                            partner: value('Routing Partner ID'),
                                            promise: value('Coverage Promise'),
                                        };
                                    }""")
                                    if result["quote"] != expected:
                                        raise AssertionError("quote gate mismatch after changing preference")
                                    if legacy and result["normalized"] != normalized:
                                        raise AssertionError("legacy paid choice normalization stale")
                                    if result["region"] != region or result["status"] != "request-only":
                                        raise AssertionError("Texas region or intake status mismatch: " + str(result))
                                    if result["partner"]:
                                        raise AssertionError("unverified Texas partner marked as assigned")
                                    if "None until" not in result["promise"]:
                                        raise AssertionError("Texas form promises unavailable pickup")
                                dimensions = page.evaluate(
                                    "() => ({page: document.documentElement.scrollWidth, window: innerWidth})"
                                )
                                if dimensions["page"] > dimensions["window"] + 8:
                                    raise AssertionError("horizontal overflow: " + str(dimensions))
                                # Test the actual submit event chain, not just a direct
                                # qualify() call. All values are invented, and the
                                # outgoing Formspree POST stays blocked by page.route.
                                if path == "/kingwood-tx-freezer-pickup/" and mode == "mobile":
                                    choice.select_option("Yes, after seeing the price")
                                    page.evaluate("""() => window.FreeReliableCustomerRouting.qualify(
                                        document.querySelector('form[action*="formspree.io"]'))""")
                                    choice.select_option("No, free pickup only")
                                    for field, value in (
                                        ("name", "VGM Synthetic Browser Test"),
                                        ("phone", "2025550200"),
                                        ("address", "123 Example Testing Street"),
                                        ("zip", "77339"),
                                        ("access_notes", "Synthetic form validation only; no real pickup"),
                                    ):
                                        form.locator('[name="' + field + '"]').fill(value)
                                    for field, value in (
                                        ("condition", "Fully working"),
                                        ("floor", "Ground floor"),
                                        ("stairs", "No stairs"),
                                        ("photos_available", "Yes"),
                                    ):
                                        form.locator('[name="' + field + '"]').select_option(label=value)
                                    if not form.evaluate("(form) => form.checkValidity()"):
                                        raise AssertionError("synthetic Kingwood test fixture invalid")
                                    # Capture a qualified customer submit event;
                                    # the intercept prevents any outbound POST.
                                    # This exercises wireForm, not just qualify().
                                    form.evaluate("""form => {
                                        if(form.dataset.customerRoutingWired !== '1')
                                            throw Error('customer submit handler not wired');
                                        window.__vgmSubmitEvents = [];
                                        form.addEventListener('submit', event => {
                                            const qualified = form.dataset.customerRoutingQualified === '1';
                                            window.__vgmSubmitEvents.push({
                                                qualified,
                                                fields: Object.fromEntries(new FormData(form).entries())
                                            });
                                            if(qualified) event.preventDefault();
                                        }, true);
                                    }""")
                                    form.locator('button[type="submit"]').click()
                                    page.wait_for_function(
                                        "() => window.__vgmSubmitEvents?.some(item => item.qualified)",
                                        timeout=12000,
                                    )
                                    events = page.evaluate("() => window.__vgmSubmitEvents")
                                    if not events or not any(item["qualified"] for item in events):
                                        raise AssertionError("qualified browser submit event was not captured")
                                    fields = {key: [str(value)] for key, value in
                                              next(item["fields"] for item in events if item["qualified"]).items()}
                                    expected_fields = {
                                        "source_page": "kingwood-tx-freezer-pickup",
                                        "state": "TX",
                                        "city": "Houston",
                                        "paid_option": "No, free pickup only",
                                        "paid_removal_preference": "free_only",
                                        "Paid Removal Quote Gate": "FREE_PICKUP_ONLY",
                                        "Routing Market Status": "request-only",
                                        "Routing Region": "Houston Metro",
                                    }
                                    for field, expected in expected_fields.items():
                                        if fields.get(field) != [expected]:
                                            raise AssertionError(
                                                "intercepted Kingwood submit mismatch: " + field
                                            )
                                    print("PASS synthetic Kingwood submit intercepted; latest free-only consent retained")
                                passed += 1
                                print("PASS", label, "photo, form, noindex, routing, quote changes")
                            except Exception as exc:
                                failure = label + " " + str(exc)
                                failures.append(failure)
                                print("FAIL", failure)
                            finally:
                                page.close()
                    finally:
                        context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print("TEXAS_DRAFT_BROWSER_PASSES", passed)
    print("TEXAS_DRAFT_BROWSER_FAILURES", len(failures))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
