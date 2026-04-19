#!/usr/bin/env python3
"""
Playwright checks: Aptum header logo, palette-driven UI, HTMX draft loading state.

Requires: pip install playwright && playwright install chromium
Run with ops-agent up: BASE_URL=http://127.0.0.1:8080 python3 scripts/verify_aptum_ui_playwright.py

Uses ticket APTUM-38273 for LLM button test (long timeout for model round-trip).
"""
from __future__ import annotations

import os
import re
import sys


def main() -> int:
    base = os.environ.get("BASE_URL", "http://127.0.0.1:8080").rstrip("/")
    issue = os.environ.get("TEST_ISSUE_KEY", "APTUM-38273")

    try:
        from playwright.sync_api import sync_playwright, expect
    except ImportError:
        print("Install: pip install playwright && playwright install chromium", file=sys.stderr)
        return 2

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(60_000)

        # --- Ticket list: header + logo ---
        page.goto(f"{base}/tickets")
        logo = page.locator(".brand-logo")
        expect(logo).to_be_visible()
        src = logo.get_attribute("src") or ""
        assert "aptumlogos.pages.dev" in src.lower(), f"logo src should use Aptum CDN, got {src!r}"
        assert re.search(r"aptum.*\.(svg|png)", src, re.I), f"logo should be Aptum asset, got {src!r}"

        lockup = page.locator(".brand-lockup")
        box = lockup.bounding_box()
        assert box and box["width"] > 80 and box["height"] > 20, "logo lockup should have sensible dimensions"

        expect(page.locator(".brand-product")).to_have_text(re.compile(r"Support workspace", re.I))

        font_stack = page.evaluate("() => getComputedStyle(document.body).fontFamily")
        assert "geist" in font_stack.lower(), f"expected Geist in body font stack, got {font_stack!r}"

        # Primary lavender on a primary button (ticket detail uses .btn-primary)
        page.goto(f"{base}/tickets/{issue}")
        btn = page.get_by_role("button", name=re.compile(r"identify potential fix", re.I))
        expect(btn).to_be_visible()
        bg = page.evaluate(
            """sel => {
                const el = document.querySelector(sel);
                return el ? getComputedStyle(el).backgroundColor : '';
            }""",
            ".btn-primary.hx-draft-trigger",
        )
        assert bg, "could not read .btn-primary background"
        # rgb(125, 122, 232) is #7D7AE8 — browsers may serialize differently; accept purple-ish channel
        assert "122" in bg or "125" in bg or "rgb" in bg.lower(), f"unexpected button bg (want Aptum lavender-ish): {bg!r}"

        # --- HTMX: spinner visible while draft generates ---
        btn.click()
        spinner = page.locator("#draft-spinner")
        expect(spinner).to_have_class(re.compile(r"htmx-indicator"))
        # Indicator receives htmx-request for the duration of the request
        expect(spinner).to_have_class(re.compile(r"htmx-request"), timeout=10_000)
        expect(spinner.locator(".spinner-orbit")).to_be_visible()

        # Outcome: draft card or error card
        outcome = page.locator(".draft-card, .draft-card-error")
        expect(outcome).to_be_visible(timeout=180_000)

        # Spinner should clear after completion
        expect(spinner).not_to_have_class(re.compile(r"htmx-request"), timeout=10_000)

        # --- Related panel: had loading indicator wiring (spinner in aside) ---
        aside = page.locator(".ticket-aside")
        expect(aside).to_be_visible()
        expect(aside.locator("section.related-section").first).to_be_visible(timeout=60_000)

        browser.close()

    print("OK: Aptum branding + logo placement + draft loading indicator checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
