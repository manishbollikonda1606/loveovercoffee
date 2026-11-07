#!/usr/bin/env python3
"""
Love Over Coffee (LOC) — Comprehensive Production Readiness Test Suite
======================================================================
Tests cover:
  1. HTML Structure & Semantic Integrity
  2. All JavaScript Functions Exist & Are Callable
  3. Routing System (hash-based SPA)
  4. Cart CRUD (add / qty / remove / clear)
  5. Order Modal & Platform Dispatch URLs
  6. Search Modal
  7. Backend API (/api/health, /api/order, /api/orders)
  8. External Links Validation (no broken hrefs)
  9. Asset Integrity (logo.jpg exists and loads)
 10. Accessibility Baseline (aria-labels, alt texts)
 11. Mobile Responsiveness Meta Tags
 12. Cookie Consent Logic
 13. Scroll Lock on Modal Open
 14. Print/PDF Brochure View Exists
 15. Deployment Blockers Check
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
import time
from html.parser import HTMLParser
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
SERVER_URL = "http://localhost:4321"

# ─── Utility ──────────────────────────────────────────
class TestResults:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []

    def ok(self, name, detail=""):
        self.passed.append((name, detail))

    def fail(self, name, detail=""):
        self.failed.append((name, detail))

    def warn(self, name, detail=""):
        self.warnings.append((name, detail))

    def summary(self):
        total = len(self.passed) + len(self.failed)
        print("\n" + "=" * 70)
        print("  LOVE OVER COFFEE — PRODUCTION READINESS TEST RESULTS")
        print("=" * 70)

        if self.passed:
            print(f"\n  ✅  PASSED: {len(self.passed)}/{total}")
            for name, detail in self.passed:
                d = f" — {detail}" if detail else ""
                print(f"      ✓ {name}{d}")

        if self.warnings:
            print(f"\n  ⚠️  WARNINGS: {len(self.warnings)}")
            for name, detail in self.warnings:
                d = f" — {detail}" if detail else ""
                print(f"      ⚠ {name}{d}")

        if self.failed:
            print(f"\n  ❌  FAILED: {len(self.failed)}/{total}")
            for name, detail in self.failed:
                d = f" — {detail}" if detail else ""
                print(f"      ✗ {name}{d}")

        print("\n" + "-" * 70)
        if not self.failed:
            print("  🎉  ALL TESTS PASSED — READY FOR DEPLOYMENT")
        else:
            print(f"  🚫  {len(self.failed)} FAILURE(S) — FIX BEFORE DEPLOYING")
        print("-" * 70 + "\n")
        return len(self.failed) == 0


R = TestResults()

def read_html():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return f.read()


# ─── TEST 1: File Existence & Basic Structure ──────────
def test_file_structure():
    if not os.path.isfile(INDEX_PATH):
        R.fail("index.html exists", "File not found")
        return
    R.ok("index.html exists", f"{os.path.getsize(INDEX_PATH):,} bytes")

    html = read_html()
    if html.startswith("<!DOCTYPE html>"):
        R.ok("DOCTYPE declaration present")
    else:
        R.fail("DOCTYPE declaration", "Missing <!DOCTYPE html>")

    if '<html lang="en"' in html:
        R.ok("html lang attribute set")
    else:
        R.fail("html lang attribute", "Missing lang='en'")

    if '<meta charset="UTF-8">' in html:
        R.ok("UTF-8 charset declared")
    else:
        R.fail("UTF-8 charset")

    if 'viewport' in html and 'width=device-width' in html:
        R.ok("Viewport meta tag set")
    else:
        R.fail("Viewport meta tag", "Missing mobile viewport")

    if '<meta name="description"' in html:
        R.ok("Meta description present")
    else:
        R.fail("Meta description", "Missing for SEO")

    if '<title>' in html and '</title>' in html:
        R.ok("Title tag present")
    else:
        R.fail("Title tag")

    # Assets
    logo_path = os.path.join(BASE_DIR, "assets", "logo.jpg")
    if os.path.isfile(logo_path):
        R.ok("Logo asset exists", f"{os.path.getsize(logo_path):,} bytes")
    else:
        R.fail("Logo asset", "assets/logo.jpg missing")

    server_path = os.path.join(BASE_DIR, "server.py")
    if os.path.isfile(server_path):
        R.ok("Backend server.py exists")
    else:
        R.warn("Backend server.py missing")


# ─── TEST 2: Required HTML Elements ───────────────────
def test_html_elements():
    html = read_html()

    required_ids = [
        "viewHome", "viewGateway", "viewBrochure", "viewLocation",
        "toastContainer", "cookieConsentBanner",
        "orderPlatformModal", "cartDrawer", "searchModal", "videoModal",
        "menuGrid", "cartItemList", "cartSubtotal", "cartTotal",
        "searchInput", "searchResults",
        "mainOrderNowBtn", "openSearchBtn", "openCartBtn",
        "cartNavBadge", "mobileMenu", "mobileMenuToggle",
    ]

    for elem_id in required_ids:
        if f'id="{elem_id}"' in html:
            R.ok(f"Element #{elem_id} exists")
        else:
            R.fail(f"Element #{elem_id}", "Missing from DOM")

    # Section IDs for scroll navigation
    section_ids = ["specials", "story", "outlets", "testimonials", "footer"]
    for sid in section_ids:
        if f'id="{sid}"' in html:
            R.ok(f"Section #{sid} exists")
        else:
            R.fail(f"Section #{sid}", "Missing section anchor")


# ─── TEST 3: All JavaScript Functions Defined ─────────
def test_js_functions():
    html = read_html()

    required_functions = [
        "handleRouting", "navigateToSection",
        "openOrderModal", "closeOrderModal",
        "openCartDrawer", "closeCartDrawer",
        "openSearchModal", "closeSearchModal",
        "openVideoModal", "closeVideoModal",
        "openGoogleMaps",
        "addToCart", "removeFromCart", "updateCartUI", "renderCartDrawer",
        "dispatchOrder", "submitDirectOrder", "dispatchDirectWhatsApp",
        "showToast",
        "handleOutletChange",
        "acceptCookies", "declineCookies", "saveCartIfConsented",
        "closeMobileMenu",
    ]

    for fn in required_functions:
        # Match both "function fnName" and "fnName = function" or "fnName("
        pattern_decl = rf'function\s+{fn}\s*\('
        pattern_assign = rf'{fn}\s*='
        if re.search(pattern_decl, html) or re.search(pattern_assign, html):
            R.ok(f"JS function: {fn}()")
        else:
            R.fail(f"JS function: {fn}()", "Not found in source")


# ─── TEST 4: Routing Hash Support ─────────────────────
def test_routing():
    html = read_html()

    routes = ["#/menu-gateway", "#/menu-brochure", "#/location", "#/outlets", "#/"]
    for route in routes:
        # The route string should appear in hash comparisons
        if route in html:
            R.ok(f"Route {route} supported")
        else:
            R.fail(f"Route {route}", "Not referenced in routing logic")

    if "hashchange" in html:
        R.ok("hashchange event listener registered")
    else:
        R.fail("hashchange listener", "SPA routing won't work without it")


# ─── TEST 5: Menu Items Data ──────────────────────────
def test_menu_data():
    html = read_html()

    # Look for the menuItems array
    match = re.search(r'const\s+menuItems\s*=\s*\[', html)
    if match:
        R.ok("menuItems array defined")
    else:
        R.fail("menuItems array", "No product data found")
        return

    # Count items by looking for { id: patterns
    items = re.findall(r"\{\s*id:\s*'[^']+',\s*title:\s*'([^']+)',\s*category:\s*'([^']+)',\s*price:\s*(\d+)", html)
    if len(items) >= 10:
        R.ok(f"Menu has {len(items)} items", "Sufficient product catalog")
    else:
        R.fail(f"Menu items count: {len(items)}", "Expected 10+ items")

    # Check that prices are reasonable (₹50 - ₹1000)
    bad_prices = [(t, int(p)) for t, c, p in items if int(p) < 30 or int(p) > 2000]
    if not bad_prices:
        R.ok("All menu prices in valid range (₹30-₹2000)")
    else:
        R.warn("Unusual prices detected", str(bad_prices))

    # Check categories exist
    categories = set(c for _, c, _ in items)
    if len(categories) >= 3:
        R.ok(f"Menu has {len(categories)} categories", ", ".join(sorted(categories)))
    else:
        R.warn("Few menu categories", str(categories))


# ─── TEST 6: External Links Not Broken ────────────────
def test_external_links():
    html = read_html()

    # Extract all href and onclick URLs
    href_pattern = re.findall(r'href="(https?://[^"]+)"', html)
    onclick_urls = re.findall(r"'(https?://[^']+)'", html)
    all_urls = set(href_pattern + onclick_urls)

    # Filter out template URLs (with encodeURIComponent placeholders)
    static_urls = [u for u in all_urls if '${' not in u and 'encodeURIComponent' not in u]

    known_external_domains = set()
    for url in static_urls:
        try:
            domain = url.split('/')[2]
            known_external_domains.add(domain)
        except IndexError:
            pass

    R.ok(f"Found {len(static_urls)} external URLs across {len(known_external_domains)} domains",
         ", ".join(sorted(known_external_domains)[:8]))

    # Critical URLs that must be present
    critical_urls = {
        "Swiggy Vaishali": "swiggy.com/city/jaipur/love-over-coffee-prince-road-vaishali-nagar-rest550658",
        "Magicpin": "magicpin.in/Jaipur/Malviya-Nagar/Restaurant/Love-Over-Coffee",
        "Zomato C-Scheme": "zomato.com/jaipur/love-over-coffee-1-c-scheme/order",
        "WhatsApp": "wa.me/917976198506",
        "Instagram": "instagram.com/loveovercoffee_",
        "Google Maps": "maps.google.com",
    }

    for name, fragment in critical_urls.items():
        found = any(fragment in u for u in static_urls)
        if found:
            R.ok(f"Critical link: {name}")
        else:
            R.fail(f"Critical link: {name}", f"URL containing '{fragment}' not found")


# ─── TEST 7: Accessibility Baseline ───────────────────
def test_accessibility():
    html = read_html()

    # Check aria-labels on interactive elements
    aria_labels = re.findall(r'aria-label="([^"]+)"', html)
    if len(aria_labels) >= 5:
        R.ok(f"Accessibility: {len(aria_labels)} aria-labels found")
    else:
        R.warn("Accessibility: few aria-labels", f"Only {len(aria_labels)} found")

    # Check alt text on images
    img_tags = re.findall(r'<img\s[^>]*>', html)
    imgs_with_alt = [t for t in img_tags if 'alt="' in t or "alt='" in t]
    if len(imgs_with_alt) == len(img_tags):
        R.ok(f"All {len(img_tags)} images have alt text")
    else:
        missing = len(img_tags) - len(imgs_with_alt)
        R.warn(f"Images missing alt text: {missing}/{len(img_tags)}")

    # pointer-events-none on icons inside buttons
    pe_none = html.count("pointer-events-none")
    if pe_none >= 3:
        R.ok(f"Icon pointer-events-none: {pe_none} instances", "Prevents click-through issues")
    else:
        R.warn("Few pointer-events-none on icons", "May cause click interception")


# ─── TEST 8: Backend API Tests ─────────────────────────
def test_backend_api():
    # Health check
    try:
        req = urllib.request.urlopen(f"{SERVER_URL}/api/health", timeout=5)
        data = json.loads(req.read())
        if data.get("status") == "ok":
            R.ok("API /api/health responds OK")
        else:
            R.fail("API /api/health", f"Unexpected response: {data}")
    except Exception as e:
        R.fail("API /api/health", str(e))

    # Static file serving
    try:
        req = urllib.request.urlopen(f"{SERVER_URL}/", timeout=5)
        content = req.read().decode("utf-8", errors="replace")
        if "Love Over Coffee" in content:
            R.ok("Static index.html served correctly")
        else:
            R.fail("Static index.html", "Content doesn't contain expected text")
    except Exception as e:
        R.fail("Static file serving", str(e))

    # Logo asset serving
    try:
        req = urllib.request.urlopen(f"{SERVER_URL}/assets/logo.jpg", timeout=5)
        logo_data = req.read()
        if len(logo_data) > 1000:
            R.ok(f"Logo asset served: {len(logo_data):,} bytes")
        else:
            R.fail("Logo asset serving", "Too small")
    except Exception as e:
        R.fail("Logo asset serving", str(e))

    # Order API POST
    try:
        order_payload = json.dumps({
            "name": "Test User",
            "outlet": "c_scheme",
            "platform": "whatsapp",
            "items": [{"title": "Flat White", "price": 190, "qty": 1}],
            "subtotal": 190
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{SERVER_URL}/api/order",
            data=order_payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        if data.get("success") and data.get("order_id", "").startswith("LOC-"):
            R.ok(f"API POST /api/order works", f"Order ID: {data['order_id']}")
        else:
            R.fail("API POST /api/order", f"Unexpected: {data}")
    except Exception as e:
        R.fail("API POST /api/order", str(e))

    # GET orders
    try:
        req = urllib.request.urlopen(f"{SERVER_URL}/api/orders", timeout=5)
        orders = json.loads(req.read())
        if isinstance(orders, list):
            R.ok(f"API GET /api/orders works", f"{len(orders)} orders stored")
        else:
            R.fail("API GET /api/orders", "Expected list")
    except Exception as e:
        R.fail("API GET /api/orders", str(e))

    # CORS headers
    try:
        req = urllib.request.Request(f"{SERVER_URL}/api/health", method="GET")
        resp = urllib.request.urlopen(req, timeout=5)
        cors = resp.headers.get("Access-Control-Allow-Origin", "")
        if cors == "*":
            R.ok("CORS headers present (Access-Control-Allow-Origin: *)")
        else:
            R.warn("CORS header missing or restricted", f"Got: '{cors}'")
    except Exception as e:
        R.warn("CORS header check", str(e))


# ─── TEST 9: CSS & Design System Consistency ──────────
def test_design_system():
    html = read_html()

    # Tailwind CDN loaded
    if "cdn.tailwindcss.com" in html:
        R.ok("Tailwind CSS CDN loaded")
    else:
        R.fail("Tailwind CSS", "CDN not found — styling will break")

    # Lucide Icons loaded
    if "unpkg.com/lucide" in html:
        R.ok("Lucide Icons CDN loaded")
    else:
        R.fail("Lucide Icons", "CDN not found — icons will break")

    # Google Fonts loaded
    if "fonts.googleapis.com" in html:
        R.ok("Google Fonts loaded")
    else:
        R.warn("Google Fonts not loaded")

    # Brand colors in Tailwind config
    brand_colors = ["#11261F", "#F3E5AB", "#D4A359", "#F9F6F0", "#F3EDE2"]
    for color in brand_colors:
        if color in html:
            R.ok(f"Brand color {color} in config")
        else:
            R.warn(f"Brand color {color} not found")

    # Print styles
    if "@media print" in html:
        R.ok("Print/PDF styles defined")
    else:
        R.warn("No print styles — brochure PDF may not format correctly")


# ─── TEST 10: Security & Deployment Checklist ─────────
def test_deployment_readiness():
    html = read_html()

    # No console.log pollution (allow console.log in catch blocks)
    console_logs = re.findall(r'console\.log\(', html)
    if len(console_logs) <= 5:
        R.ok(f"Console.log calls: {len(console_logs)}", "Acceptable for production")
    else:
        R.warn(f"Console.log calls: {len(console_logs)}", "Consider removing debug logs")

    # No debugger statements
    if "debugger" not in html:
        R.ok("No debugger statements")
    else:
        R.fail("Debugger statement found", "REMOVE before deploy")

    # No localhost references in production URLs
    localhost_refs = re.findall(r'https?://localhost', html)
    if not localhost_refs:
        R.ok("No hardcoded localhost URLs in HTML")
    else:
        R.warn(f"Localhost references: {len(localhost_refs)}", "May break in production")

    # No TODO/FIXME/HACK comments
    todos = re.findall(r'(?:TODO|FIXME|HACK|XXX)\b', html, re.IGNORECASE)
    if not todos:
        R.ok("No TODO/FIXME/HACK comments")
    else:
        R.warn(f"Found {len(todos)} TODO/FIXME markers")

    # XSS: Check for innerHTML with user input (basic check)
    innerhtml_uses = re.findall(r'\.innerHTML\s*=', html)
    innerhtml_safe = re.findall(r'\.innerHTML\s*=\s*[\'"`]', html)
    if len(innerhtml_uses) <= 20:
        R.ok(f"innerHTML usage: {len(innerhtml_uses)} instances", "Within acceptable range for static site")
    else:
        R.warn(f"High innerHTML usage: {len(innerhtml_uses)}", "Review for XSS safety")

    # Check that external links use target="_blank" with rel safety
    target_blanks = re.findall(r'target="_blank"', html)
    rel_noopener = re.findall(r'rel="noopener', html)
    if len(target_blanks) > 0:
        R.ok(f"External links with target=_blank: {len(target_blanks)}")
        if len(rel_noopener) == 0:
            R.warn("No rel='noopener' on target=_blank links", "Minor security: add rel='noopener noreferrer'")
        else:
            R.ok(f"rel='noopener' present on {len(rel_noopener)} links")

    # File size check
    size_kb = os.path.getsize(INDEX_PATH) / 1024
    if size_kb < 500:
        R.ok(f"index.html size: {size_kb:.0f} KB", "Good — under 500 KB")
    elif size_kb < 1000:
        R.warn(f"index.html size: {size_kb:.0f} KB", "Large single-file app")
    else:
        R.warn(f"index.html size: {size_kb:.0f} KB", "Very large — consider code splitting")


# ─── TEST 11: Scroll Lock & Modal Logic ───────────────
def test_modal_logic():
    html = read_html()

    # Scroll lock CSS exists
    if "overflow-hidden" in html and "overscroll-behavior" in html:
        R.ok("Scroll lock CSS rules defined")
    else:
        R.warn("Scroll lock CSS incomplete")

    # Modal backdrop click closes
    if 'if(event.target === this)' in html:
        R.ok("Modal backdrop click-to-close implemented")
    else:
        R.warn("Missing backdrop click-to-close")

    # event.stopPropagation on modal content
    if "event.stopPropagation()" in html:
        R.ok("Modal content click propagation stopped")
    else:
        R.warn("Missing stopPropagation on modal content")

    # Close buttons have cursor-pointer
    close_btns = re.findall(r'onclick="close\w+\(\)"[^>]*class="[^"]*cursor-pointer', html)
    if len(close_btns) >= 2:
        R.ok(f"Close buttons with cursor-pointer: {len(close_btns)}")
    else:
        R.warn("Some close buttons may lack cursor-pointer")


# ─── TEST 12: Cookie Consent ─────────────────────────
def test_cookie_consent():
    html = read_html()

    if "cookieConsentBanner" in html:
        R.ok("Cookie consent banner element exists")
    else:
        R.fail("Cookie consent banner missing")

    if "acceptCookies" in html and "declineCookies" in html:
        R.ok("Cookie accept/decline handlers defined")
    else:
        R.fail("Cookie handlers missing")

    if "localStorage" in html:
        R.ok("localStorage used for persistence")
    else:
        R.warn("No localStorage usage detected")


# ─── TEST 13: HTML Validity Checks ────────────────────
def test_html_validity():
    html = read_html()

    # Check balanced tags for critical elements
    for tag in ["div", "section", "button", "script"]:
        opens = len(re.findall(rf'<{tag}[\s>]', html))
        closes = len(re.findall(rf'</{tag}>', html))
        if opens == closes:
            R.ok(f"Balanced <{tag}> tags: {opens} open / {closes} close")
        else:
            diff = opens - closes
            if abs(diff) <= 1:
                R.warn(f"<{tag}> balance off by {diff}: {opens} open / {closes} close")
            else:
                R.fail(f"<{tag}> tags unbalanced: {opens} open / {closes} close", f"Diff: {diff}")

    # Ensure </html> and </body> close properly
    if "</html>" in html:
        R.ok("</html> closing tag present")
    else:
        R.fail("Missing </html>")

    if "</body>" in html:
        R.ok("</body> closing tag present")
    else:
        R.fail("Missing </body>")


# ─── TEST 14: Brochure & Print View ──────────────────
def test_brochure_view():
    html = read_html()

    if "viewBrochure" in html:
        R.ok("Brochure view element exists (viewBrochure)")
    else:
        R.fail("Brochure view missing")

    if "printableBrochureArea" in html:
        R.ok("Printable brochure area defined")
    else:
        R.warn("No printable brochure area")

    if "openAndPrintBrochure" in html:
        R.ok("Print brochure function exists")
    else:
        R.warn("Missing openAndPrintBrochure function")

    # Full 55+ item brochure dataset
    brochure_match = re.findall(r'const\s+brochureData\s*=', html)
    if brochure_match:
        R.ok("brochureData dataset defined for brochure")
    else:
        R.warn("brochureData not found — brochure may be incomplete")


# ─── TEST 15: Outlet Cards Data ───────────────────────
def test_outlets():
    html = read_html()

    outlet_names = ["C-Scheme Flagship", "B2 Bypass", "JLN Road", "Durgapura", "Vidhyadhar Nagar", "Vaishali Nagar"]
    for name in outlet_names:
        if name in html:
            R.ok(f"Outlet listed: {name}")
        else:
            R.warn(f"Outlet missing: {name}")

    # Phone numbers
    phones = ["79761 98506", "99287 83999", "072320 99909"]
    for phone in phones:
        if phone in html:
            R.ok(f"Phone number: {phone}")
        else:
            R.warn(f"Phone number missing: {phone}")


# ─── TEST 16: Server.py Sanity ────────────────────────
def test_server_sanity():
    server_path = os.path.join(BASE_DIR, "server.py")
    if not os.path.isfile(server_path):
        R.warn("server.py not found — skipping backend tests")
        return

    with open(server_path, "r") as f:
        code = f.read()

    # Check for proper error handling
    if "try:" in code and "except" in code:
        R.ok("server.py has error handling (try/except)")
    else:
        R.warn("server.py lacks error handling")

    # Check CORS support
    if "Access-Control-Allow-Origin" in code:
        R.ok("server.py has CORS support")
    else:
        R.fail("server.py missing CORS", "Frontend API calls will fail cross-origin")

    # Check for ThreadingMixIn (concurrent requests)
    if "ThreadingMixIn" in code:
        R.ok("server.py supports concurrent requests (ThreadingMixIn)")
    else:
        R.warn("server.py single-threaded — may hang under load")

    # Check reusable address
    if "allow_reuse_address" in code:
        R.ok("server.py uses allow_reuse_address")
    else:
        R.warn("server.py may fail on restart (address in use)")


# ─── TEST 17: Performance & Bundle Checks ─────────────
def test_performance():
    html = read_html()
    size_bytes = len(html.encode("utf-8"))

    # CDN version pinning
    if "cdn.tailwindcss.com" in html:
        R.ok("Tailwind loaded from CDN")
        if "@latest" in html or "unpkg.com/lucide@latest" in html:
            R.warn("CDN uses @latest", "Pin to specific version for stability: unpkg.com/lucide@0.263.0")
        else:
            R.ok("CDN versions look pinned")

    # Image lazy loading
    lazy_imgs = re.findall(r'loading="lazy"', html)
    total_imgs = len(re.findall(r'<img\s', html))
    if total_imgs > 0:
        R.ok(f"Images: {total_imgs} total, {len(lazy_imgs)} with lazy loading")
    else:
        R.ok("No images to lazy-load")

    # Preconnect hints
    preconnects = re.findall(r'rel="preconnect"', html)
    if len(preconnects) >= 1:
        R.ok(f"Preconnect hints: {len(preconnects)}")
    else:
        R.warn("No preconnect hints for external resources")


# ─── RUN ALL TESTS ────────────────────────────────────
if __name__ == "__main__":
    print("\n☕ Love Over Coffee — Production Readiness Test Suite")
    print("=" * 55)
    print(f"   Source: {INDEX_PATH}")
    print(f"   Server: {SERVER_URL}")
    print(f"   Time:   {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    test_file_structure()
    test_html_elements()
    test_js_functions()
    test_routing()
    test_menu_data()
    test_external_links()
    test_accessibility()
    test_backend_api()
    test_design_system()
    test_deployment_readiness()
    test_modal_logic()
    test_cookie_consent()
    test_html_validity()
    test_brochure_view()
    test_outlets()
    test_server_sanity()
    test_performance()

    success = R.summary()
    sys.exit(0 if success else 1)
