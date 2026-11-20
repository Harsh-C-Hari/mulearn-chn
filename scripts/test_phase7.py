#!/usr/bin/env py
"""
µLearn CHN — Phase 7 Automated Verification Suite
Tests the memory asset audit, 6-frame editorial collage, 11-item community gallery,
drawer toggle, category filtering, section structure, navigation anchors,
content rules, and multi-viewport responsive layout.
"""
import os, sys, re, json, subprocess, time
from PIL import Image
from playwright.sync_api import sync_playwright

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PORT = "8775"
URL = f"http://localhost:{PORT}/index.html"

out = {"checks": [], "passed": 0, "failed": 0}

def chk(name, ok, detail=""):
    out["checks"].append({"name": name, "ok": bool(ok), "detail": str(detail) if not ok else ""})
    if ok:
        out["passed"] += 1
        print(f"PASS {name}")
    else:
        out["failed"] += 1
        print(f"FAIL {name}: {detail}", file=sys.stderr)
    sys.stdout.flush()

srv = subprocess.Popen([sys.executable, "-m", "http.server", PORT], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

try:
    # 1. Asset & Data Audit
    with open(os.path.join(root, "data", "memories.js"), "r", encoding="utf-8") as f:
        mem_code = f.read()

    chk("no source assets in data/memories.js", "sources/" not in mem_code)
    chk("rejected asset event5_zdu88j excluded from data/memories.js", "event5_zdu88j" not in mem_code)

    # Node data inspection
    node_cmd = [
        "node", "-e",
        """
        global.window = {};
        require('./data/memories.js');
        console.log(JSON.stringify(window.MULEARN.memories));
        """
    ]
    raw_json = subprocess.check_output(node_cmd, cwd=root, text=True)
    mem_data = json.loads(raw_json)

    chk("collage contains exactly 6 items", len(mem_data.get("collage", [])) == 6, len(mem_data.get("collage", [])))
    chk("gallery contains exactly 11 items", len(mem_data.get("gallery", [])) == 11, len(mem_data.get("gallery", [])))

    # Generator check
    gen_rc = subprocess.call(["node", "scripts/build_memories.js", "--check"], cwd=root)
    chk("index.html memories markup is generated from data", gen_rc == 0)

    # Verify physical collage derivatives
    bad_collage = []
    for c in mem_data.get("collage", []):
        for k in ("src460", "src920", "src1200"):
            if k in c:
                p = os.path.join(root, c[k])
                if not os.path.exists(p):
                    bad_collage.append(c[k])
                else:
                    im = Image.open(p)
                    if im.format != "WEBP":
                        bad_collage.append(f"{c[k]} format {im.format}")
    chk("all collage derivatives exist on disk and are WebP", not bad_collage, bad_collage)

    # Verify physical gallery derivatives
    bad_gallery = []
    gallery_ids = set()
    for g in mem_data.get("gallery", []):
        gallery_ids.add(g["id"])
        p = os.path.join(root, g["src"])
        if not os.path.exists(p):
            bad_gallery.append(g["src"])
        else:
            im = Image.open(p)
            if im.format != "WEBP":
                bad_gallery.append(f"{g['src']} format {im.format}")
            if im.size != (g["width"], g["height"]):
                bad_gallery.append(f"{g['src']} size mismatch: real {im.size} vs recorded {(g['width'], g['height'])}")
    chk("all 11 gallery images exist on disk, are WebP, and match recorded dimensions", not bad_gallery, bad_gallery)

    # 2. Browser Verification across 5 viewports
    with sync_playwright() as p:
        browser = p.chromium.launch()

        for width in (320, 390, 768, 1024, 1440):
            page = browser.new_page(viewport={"width": width, "height": 900})
            errors = []
            ext_reqs = []

            page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.on("request", lambda req: ext_reqs.append(req.url) if not req.url.startswith((f"http://localhost:{PORT}", "data:")) else None)

            page.goto(URL)
            page.wait_for_timeout(600)

            # Check horizontal overflow
            scroll_w = page.evaluate("document.documentElement.scrollWidth")
            inner_w = page.evaluate("window.innerWidth")
            chk(f"{width}px: no horizontal overflow (scrollWidth {scroll_w} <= window {inner_w})", scroll_w <= inner_w, (scroll_w, inner_w))
            chk(f"{width}px: no console errors", not errors, errors)
            chk(f"{width}px: no external requests", not ext_reqs, ext_reqs)

            # Check collage rendering
            frames_count = page.evaluate("document.querySelectorAll('#memories-collage .polaroid').length")
            chk(f"{width}px: exactly 6 collage polaroid frames rendered", frames_count == 6, frames_count)

            # Check gallery cards rendering (11 cards)
            cards_count = page.evaluate("document.querySelectorAll('#memories-gallery .gallery-card').length")
            chk(f"{width}px: exactly 11 gallery cards rendered", cards_count == 11, cards_count)

            if width == 1440:
                # Semantic structure
                chk("#memories is a <section> element", page.evaluate("document.getElementById('memories').tagName === 'SECTION'"))
                chk("#memories is labelled by h2#memories-title", page.evaluate("""
                    (()=>{
                        const s = document.getElementById('memories');
                        const h = document.getElementById('memories-title');
                        return s.getAttribute('aria-labelledby') === 'memories-title' && h && h.tagName === 'H2';
                    })()
                """))

                # Section order
                sec_order = page.evaluate("""
                    [...document.querySelectorAll('main > section, footer')].map(e => e.id || e.className.split(' ')[0])
                """)
                expected_order = ["hero", "about", "offers", "events", "team", "memories", "join", "site-footer"]
                chk("section order hero -> about -> offers -> events -> team -> memories -> join -> site-footer", sec_order == expected_order, sec_order)

                # Navigation targets
                nav_href = page.evaluate("document.querySelector('header .site-nav__link[href=\"#memories\"]') !== null")
                chk("header nav link href='#memories' exists", nav_href)

                about_cta = page.evaluate("document.querySelector('.about a[href=\"#memories\"]') !== null")
                chk("About 'Our journey' CTA href='#memories' exists", about_cta)

                footer_link = page.evaluate("document.querySelector('footer a[href=\"#memories\"]') !== null")
                chk("footer nav link href='#memories' exists", footer_link)

                # Collage details
                slots = page.evaluate("""
                    [...document.querySelectorAll('#memories-collage .polaroid')].map(f => f.dataset.slot)
                """)
                chk("collage slots are p1 through p6", slots == ["p1", "p2", "p3", "p4", "p5", "p6"], slots)

                main_slot = page.evaluate("""
                    document.querySelector('#memories-collage .polaroid--main').dataset.slot
                """)
                chk("main polaroid is p5 (community group photo)", main_slot == "p5", main_slot)

                # Check lightbox target links in collage
                collage_targets = page.evaluate("""
                    [...document.querySelectorAll('#memories-collage .polaroid__action')].map(b => b.dataset.lightboxOpen)
                """)
                chk("all collage buttons target valid lightbox IDs", all(t in gallery_ids for t in collage_targets), collage_targets)

                # Check lightbox target links in gallery
                gallery_targets = page.evaluate("""
                    [...document.querySelectorAll('#memories-gallery .gallery-card__action')].map(b => b.dataset.lightboxOpen)
                """)
                chk("all gallery buttons target valid lightbox IDs", all(t in gallery_ids for t in gallery_targets), gallery_targets)

                # Test 7.3 Interactive Drawer Toggle
                toggle_btn = page.locator("#memories-gallery-toggle")
                drawer = page.locator("#memories-gallery")

                init_expanded = toggle_btn.get_attribute("aria-expanded")
                init_hidden = drawer.get_attribute("hidden")
                chk("drawer starts closed (aria-expanded='false', hidden present)", init_expanded == "false" and init_hidden is not None)

                toggle_btn.click()
                page.wait_for_timeout(300)
                open_expanded = toggle_btn.get_attribute("aria-expanded")
                open_hidden = drawer.get_attribute("hidden")
                chk("clicking toggle opens drawer (aria-expanded='true', hidden removed)", open_expanded == "true" and open_hidden is None)

                # Test 7.3 Category Filtering
                # Click 'workshops' filter
                page.click(".gallery-filter[data-filter='workshops']")
                page.wait_for_timeout(200)
                workshops_vis = page.evaluate("""
                    [...document.querySelectorAll('#memories-gallery .gallery-card:not([hidden])')].length
                """)
                chk("filtering by workshops shows exactly 4 cards", workshops_vis == 4, workshops_vis)

                # Click 'events' filter
                page.click(".gallery-filter[data-filter='events']")
                page.wait_for_timeout(200)
                events_vis = page.evaluate("""
                    [...document.querySelectorAll('#memories-gallery .gallery-card:not([hidden])')].length
                """)
                chk("filtering by events shows exactly 5 cards", events_vis == 5, events_vis)

                # Click 'all' filter
                page.click(".gallery-filter[data-filter='all']")
                page.wait_for_timeout(200)
                all_vis = page.evaluate("""
                    [...document.querySelectorAll('#memories-gallery .gallery-card:not([hidden])')].length
                """)
                chk("filtering by all restores all 11 cards", all_vis == 11, all_vis)

                # Toggle drawer closed
                toggle_btn.click()
                page.wait_for_timeout(200)
                closed_expanded = toggle_btn.get_attribute("aria-expanded")
                closed_hidden = drawer.get_attribute("hidden")
                chk("re-clicking toggle closes drawer (aria-expanded='false', hidden present)", closed_expanded == "false" and closed_hidden is not None)

                # Test 7.4 Reusable Accessible Lightbox
                lb_dlg = page.locator("#memories-lightbox")
                lb_is_open = page.evaluate("document.getElementById('memories-lightbox').hasAttribute('open')")
                chk("lightbox starts closed", not lb_is_open)

                # Open from collage polaroid p1 (target: lightbox-img-7834)
                p1_btn = page.locator('.polaroid[data-slot="p1"] .polaroid__action')
                p1_btn.click()
                page.wait_for_timeout(300)

                chk("clicking collage polaroid opens lightbox", page.evaluate("document.getElementById('memories-lightbox').hasAttribute('open')"))
                active_src = page.evaluate("document.getElementById('lightbox-image').getAttribute('src')")
                chk("active photo src matches target", "lightbox-img-7834" in active_src, active_src)
                active_counter = page.evaluate("document.getElementById('lightbox-counter').innerText")
                chk("counter displays photo position (Photo 3 of 11)", "3 of 11" in active_counter, active_counter)

                # Step Next via button
                page.click("#lightbox-next")
                page.wait_for_timeout(200)
                next_src = page.evaluate("document.getElementById('lightbox-image').getAttribute('src')")
                chk("clicking next steps to photo 4 (lightbox-img-7844)", "lightbox-img-7844" in next_src, next_src)

                # Step via Keyboard ArrowLeft / ArrowRight
                page.keyboard.press("ArrowLeft")
                page.wait_for_timeout(200)
                arrow_src = page.evaluate("document.getElementById('lightbox-image').getAttribute('src')")
                chk("ArrowLeft steps back to photo 3", "lightbox-img-7834" in arrow_src, arrow_src)

                page.keyboard.press("ArrowRight")
                page.wait_for_timeout(200)
                arrow_right_src = page.evaluate("document.getElementById('lightbox-image').getAttribute('src')")
                chk("ArrowRight steps forward to photo 4", "lightbox-img-7844" in arrow_right_src, arrow_right_src)

                # Close via Escape key & verify focus return
                page.keyboard.press("Escape")
                page.wait_for_timeout(300)
                lb_closed_esc = not page.evaluate("document.getElementById('memories-lightbox').hasAttribute('open')")
                focus_returned_p1 = page.evaluate("document.activeElement.getAttribute('data-lightbox-open') === 'lightbox-img-7834'")
                chk("Escape closes lightbox and returns focus to polaroid trigger", lb_closed_esc and focus_returned_p1, (lb_closed_esc, focus_returned_p1))

                # Open from gallery card (photo-odyssey-wrap)
                # First open drawer
                toggle_btn.click()
                page.wait_for_timeout(200)
                ody_btn = page.locator('.gallery-card[data-id="photo-odyssey-wrap"] .gallery-card__action')
                ody_btn.click()
                page.wait_for_timeout(300)
                chk("clicking gallery card opens lightbox", page.evaluate("document.getElementById('memories-lightbox').hasAttribute('open')"))
                ody_src = page.evaluate("document.getElementById('lightbox-image').getAttribute('src')")
                chk("active photo matches event photo", "photo-odyssey-wrap" in ody_src, ody_src)
                ody_cat = page.evaluate("document.getElementById('lightbox-category').innerText")
                chk("category badge matches event name", ody_cat == "ODYSSEY", ody_cat)

                # Close via Close button
                page.click("#lightbox-close")
                page.wait_for_timeout(300)
                lb_closed_btn = not page.evaluate("document.getElementById('memories-lightbox').hasAttribute('open')")
                focus_returned_ody = page.evaluate("document.activeElement.getAttribute('data-lightbox-open') === 'photo-odyssey-wrap'")
                chk("Close button closes lightbox and returns focus to gallery card trigger", lb_closed_btn and focus_returned_ody, (lb_closed_btn, focus_returned_ody))

                # Close drawer
                toggle_btn.click()
                page.wait_for_timeout(200)

                # Text rules inside memories
                mem_text = page.evaluate("document.getElementById('memories').innerText")
                chk("no Greek mu in memories text", "μ" not in mem_text and "Μ" not in mem_text)
                chk("no invented stats in memories text", not re.search(r"\d+\+?\s*(members|learners|events)", mem_text))

            page.close()

        browser.close()

finally:
    srv.terminate()

print(f"\nPhase 7 Results: {out['passed']} passed, {out['failed']} failed")
if out["failed"] > 0:
    sys.exit(1)
