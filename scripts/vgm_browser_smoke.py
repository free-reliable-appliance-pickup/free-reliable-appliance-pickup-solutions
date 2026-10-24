#!/usr/bin/env python3
"""Read-only Playwright smoke tests for VGM priority pages.

Runs against the checked-out site on a local HTTP server. Never submits a
customer form, uses a real customer address, or writes to production.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ("/", "Home"),
    ("/los-angeles-appliance-pickup/", "Los Angeles"),
    ("/rancho-cucamonga-appliance-pickup/", "Rancho Cucamonga"),
    ("/fontana-appliance-pickup/", "Fontana"),
    ("/san-fernando-appliance-pickup/", "San Fernando"),
]
VIEWPORTS = [
    ("desktop", {"width": 1365, "height": 900}),
    ("mobile", {"width": 390, "height": 844}),
]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def run():
    handler = partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = "http://127.0.0.1:" + str(server.server_port)
    failures = []
    checks = 0
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                for viewport_name, viewport in VIEWPORTS:
                    context = browser.new_context(viewport=viewport)
                    try:
                        for path, label in PAGES:
                            page = context.new_page()
                            try:
                                response = page.goto(base + path, wait_until="domcontentloaded", timeout=30000)
                                if response is None or response.status != 200:
                                    raise AssertionError("page did not return HTTP 200")
                                page.locator("h1").first.wait_for(state="visible", timeout=15000)
                                if page.locator("#request").count() == 0:
                                    raise AssertionError("pickup request target #request is missing")
                                if page.locator("#request form").count() == 0:
                                    raise AssertionError("pickup request form is missing")
                                if not page.locator("form[action*='formspree.io']").count():
                                    raise AssertionError("no Formspree form action found")
                                # Decode the actual above-the-fold appliance image, not only its HTML src.
                                # This detects missing, corrupt or unreachable local image files.
                                hero_image = page.locator("main img").first
                                if hero_image.count() == 0:
                                    raise AssertionError("no main appliance image found")
                                hero_image.scroll_into_view_if_needed(timeout=10000)
                                decoded_width = hero_image.evaluate(
                                    "(img) => img.decode().then(() => img.naturalWidth).catch(() => 0)"
                                )
                                if decoded_width < 100:
                                    raise AssertionError(
                                        "main appliance image failed to load: "
                                        + str(hero_image.get_attribute("src"))
                                    )
                                # Browser-interact with both paid-quote preference options.
                                # This never clicks the submit button and never transmits lead data.
                                quote_choice = page.locator("#request select[name='paid_removal_preference']")
                                if quote_choice.count() != 1:
                                    raise AssertionError("paid removal preference is missing or ambiguous")
                                quote_choice.select_option("quote_ok")
                                if quote_choice.input_value() != "quote_ok":
                                    raise AssertionError("paid removal quote choice did not persist")
                                quote_choice.select_option("free_only")
                                if quote_choice.input_value() != "free_only":
                                    raise AssertionError("free-only preference did not persist")
                                # We deliberately do not submit any form or use customer data.
                                if path == "/":
                                    zip_input = page.locator("#hero-zip")
                                    zip_input.fill("12")
                                    if zip_input.evaluate("(el) => el.checkValidity()"):
                                        raise AssertionError("invalid ZIP incorrectly passes validation")
                                checks += 1
                                dimensions = page.evaluate(
                                    "() => ({width: document.documentElement.scrollWidth, viewport: innerWidth})"
                                )
                                if dimensions["width"] > dimensions["viewport"] + 5:
                                    print(
                                        "REVIEW: horizontal overflow on",
                                        label, viewport_name, dimensions,
                                    )
                                print("PASS:", label, viewport_name, "HTTP 200, heading, form, image, quote selection")
                            except Exception as exc:
                                failures.append(label + " / " + viewport_name + ": " + str(exc))
                                print("FAIL:", failures[-1])
                            finally:
                                page.close()
                    finally:
                        context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print("VGM browser smoke:", checks, "passed;", len(failures), "failed")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
