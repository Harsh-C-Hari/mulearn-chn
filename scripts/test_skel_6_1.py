#!/usr/bin/env python3
"""6.1 — full regression with the skeleton system active: loading modes (slow/normal/cached/lazy/failed/dynamic),
existing features (nav, event dialogs, team directory, gallery filters, lightbox) while skeletons are showing, console/network cleanliness."""
import sys, os, json, functools, time
sys.path.insert(0, os.path.dirname(__file__))
from skel_harness import *
from playwright.sync_api import sync_playwright
print = functools.partial(print, flush=True)
OUT = os.path.join(ROOT, 'docs', 'screenshots'); res = {}; ok = True
def check(n, c, i=''):
    global ok; ok = ok and bool(c); res[n] = {'pass': bool(c), 'info': str(i)[:400]}; print(('PASS ' if c else 'FAIL ') + n, str(i)[:240])
def watch(pg, errs, ext, base):
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text and 'ERR_FAILED' not in m.text else None)
    pg.on('request', lambda r: ext.append(r.url) if not r.url.startswith(base) and not r.url.startswith('data:') else None)
srv, url = serve()
with sync_playwright() as p:
    b = p.chromium.launch()

    # ---- 1. loading modes ----
    # normal (no interception)
    pg = b.new_page(viewport={'width': 1440, 'height': 900}); errs = []; ext = []; watch(pg, errs, ext, url); pg.set_default_timeout(10000)
    pg.goto(url + '/index.html', wait_until='load'); pg.wait_for_timeout(2500)
    vis_left = pg.evaluate("[...document.querySelectorAll('.skel')].filter(s=>{const r=s.getBoundingClientRect();return r.width>0&&r.bottom>0&&r.top<innerHeight}).length")
    check('1a normal loading: no skeleton left in view, 0 console/page errors, 0 external requests', vis_left == 0 and not errs and not ext, {'left': vis_left, 'errs': errs[:2], 'ext': ext[:2]})
    # lazy: scroll down, every skeleton disappears as its image arrives
    H = pg.evaluate("document.documentElement.scrollHeight")
    for y in range(0, H, 700): pg.evaluate("y=>window.scrollTo(0,y)", y); pg.wait_for_timeout(120)
    pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); pg.wait_for_timeout(300)
    H = pg.evaluate("document.documentElement.scrollHeight")
    for y in range(0, H, 600): pg.evaluate("y=>window.scrollTo(0,y)", y); pg.wait_for_timeout(120)
    pg.wait_for_timeout(1500)
    left = pg.evaluate("[...document.querySelectorAll('.skel')].map(s=>s.className.split(' ')[1])")
    imgs = pg.evaluate("[...document.querySelectorAll('img')].filter(i=>i.getAttribute('src')&&i.id!=='lightbox-image'&&i.getBoundingClientRect().width>0&&!(i.complete&&i.naturalWidth>0)).map(i=>i.currentSrc||i.src)")
    check('1b lazy images: after scrolling the whole page no overlay remains and every visible image decoded', not left and not imgs, {'left': left[:3], 'imgs': imgs[:3]})
    check('1c no console/page errors during full scroll', not errs, errs[:3]); pg.close()
    # slow (each image 400 ms)
    pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.set_default_timeout(15000); delay(pg, 400)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(450)
    seen = pg.evaluate("document.querySelectorAll('.skel').length")
    pg.wait_for_timeout(6000)
    vis_left = pg.evaluate("[...document.querySelectorAll('.skel')].filter(s=>{const r=s.getBoundingClientRect();return r.width>0&&r.bottom>0&&r.top<innerHeight}).length")
    check('1d slow loading (400 ms/img): skeletons appear, then all in-view ones are gone', seen > 0 and vis_left == 0, {'seen': seen, 'left': vis_left}); close_page(pg)
    # failed
    pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.set_default_timeout(10000); errs = []; watch(pg, errs, [], url); fail(pg)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(2500)
    f = pg.evaluate("[...document.querySelectorAll('.skel')].filter(s=>{const r=s.getBoundingClientRect();return r.width>0&&r.bottom>0&&r.top<innerHeight}).map(s=>s.classList.contains('is-failed'))")
    check('1e failed images: every in-view overlay is the static failed state, no page errors', f and all(f) and not errs, {'n': len(f), 'errs': errs[:2]}); close_page(pg)

    # ---- 2. existing features while skeletons are showing (all image requests held) ----
    for w, h in ((390, 844), (1440, 900)):
        pg = b.new_page(viewport={'width': w, 'height': h}); pg.set_default_timeout(10000); errs = []; watch(pg, errs, [], url); hold(pg)
        pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1800)
        # navigation: anchors scroll to their sections (menu first on mobile)
        if w < 1180:
            pg.click('[data-js="nav-toggle"], .nav-toggle, button[aria-controls="site-nav"]'); pg.wait_for_timeout(300)
        pg.click('#site-nav a[href="#team"]'); pg.wait_for_timeout(1500)
        top = pg.evaluate("document.getElementById('team').getBoundingClientRect().top")
        check(f'2a {w}: nav link scrolls to #team with skeletons showing', abs(top) < 200, round(top))
        # team directory: roster present, skeleton per row, names visible, no overlap of text by overlay
        r = pg.evaluate("({rows:document.querySelectorAll('.roster__photo').length,sk:document.querySelectorAll('.skel--roster').length,txt:[...document.querySelectorAll('.roster li')].slice(0,3).map(l=>l.textContent.trim().slice(0,20))})")
        check(f'2b {w}: team directory 21 rows, each with a skeleton, text intact', r['rows'] == 21 and r['sk'] == 21 and all(r['txt']), r)
        # event dialog: open with held photo, skeleton shows, Esc closes, reopen has no duplicates
        pg.evaluate("document.getElementById('events').scrollIntoView()"); pg.wait_for_timeout(500)
        btn = pg.locator('[data-event-open="odyssey"]').first; btn.scroll_into_view_if_needed(); btn.click(); pg.wait_for_timeout(700)
        d = pg.evaluate("({open:document.getElementById('event-dialog').open,sk:document.querySelectorAll('#event-dialog .skel').length,t:document.getElementById('event-dialog-title').textContent.trim()})")
        check(f'2c {w}: event dialog opens with content; photo skeleton present', d['open'] and d['t'] and d['sk'] >= 1, d)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        check(f'2d {w}: Esc closes dialog, focus returns to the trigger', not pg.evaluate("document.getElementById('event-dialog').open") and pg.evaluate("!!document.activeElement.closest('[data-event-open]')"))
        btn.click(); pg.wait_for_timeout(500)
        check(f'2e {w}: re-open: one skeleton per photo (no duplicates)', pg.evaluate("(()=>{const ph=document.querySelectorAll('#event-dialog .event-dialog__photo img').length;return document.querySelectorAll('#event-dialog .skel').length===ph})()"))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        # gallery filters
        pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); pg.wait_for_timeout(400)
        counts = {}
        for flt in ('all', 'workshops', 'events', 'design', 'community'):
            bt = pg.locator(f'.gallery-filter[data-filter="{flt}"]').first
            bt.scroll_into_view_if_needed(); bt.click(); pg.wait_for_timeout(250)
            counts[flt] = pg.evaluate("[...document.querySelectorAll('.gallery-card')].filter(c=>!c.hidden).length")
        check(f'2f {w}: gallery filters change the visible set (11/4/5/1/1) with skeletons present', counts == {'all': 11, 'workshops': 4, 'events': 5, 'design': 1, 'community': 1}, counts)
        pg.locator('.gallery-filter[data-filter="all"]').first.click(); pg.wait_for_timeout(250)
        # lightbox via gallery card, next/prev buttons
        pg.locator('.gallery-card__action').first.scroll_into_view_if_needed(); pg.locator('.gallery-card__action').first.click(); pg.wait_for_timeout(500)
        t0 = pg.evaluate("document.getElementById('lightbox-title').textContent")
        nb = '#lightbox-next'; pb = '#lightbox-prev'   # the mobile pair is display:none at every tested width (5.3 hit-test)
        pg.click(nb); pg.wait_for_timeout(300); t1 = pg.evaluate("document.getElementById('lightbox-title').textContent")
        pg.click(pb); pg.wait_for_timeout(300); t2 = pg.evaluate("document.getElementById('lightbox-title').textContent")
        check(f'2g {w}: lightbox next/prev work while the skeleton shows', t0 and t1 != t0 and t2 == t0, [t0, t1, t2])
        check(f'2h {w}: 0 page errors across all interactions', not errs, errs[:3])
        close_page(pg)

    # ---- 3. existing animations / reduced motion intact ----
    pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.set_default_timeout(10000)
    pg.goto(url + '/index.html', wait_until='load'); pg.wait_for_timeout(2500)
    check('3a GSAP motion still active (html.js-motion) and skeleton CSS did not disable it', pg.evaluate("document.documentElement.classList.contains('js-motion')"))
    pg.close()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce'); pg = ctx.new_page(); pg.set_default_timeout(10000)
    pg.goto(url + '/index.html', wait_until='load'); pg.wait_for_timeout(1500)
    check('3b reduced motion: js-motion off and 0 skeleton animations', not pg.evaluate("document.documentElement.classList.contains('js-motion')") and pg.evaluate("document.getAnimations().filter(a=>a.effect&&a.effect.target&&a.effect.target.closest&&a.effect.target.closest('.skel,[data-skel-reveal]')).length") == 0)
    ctx.close()

    # ---- 4. performance observations (not pass/fail judgements of the page, only of the skeleton's footprint) ----
    sz = {f: os.path.getsize(os.path.join(ROOT, f)) for f in ('js/skeleton.js', 'css/skeleton.css')}
    check('4a footprint: skeleton.js + skeleton.css < 30 KB raw, 0 new assets/dependencies', sum(sz.values()) < 30000 and not os.path.exists(os.path.join(ROOT, 'img/skeleton')), sz)
    pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.set_default_timeout(15000)
    pg.add_init_script("window.__lcp=0;new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true})")
    pg.goto(url + '/index.html', wait_until='load'); pg.wait_for_timeout(2500)
    perf = pg.evaluate("({lcp:Math.round(window.__lcp),skelNodes:document.querySelectorAll('.skel').length,heap:0})")
    pb = b.new_page(viewport={'width': 1440, 'height': 900}); pb.set_default_timeout(15000); pb.route('**/js/skeleton.js', lambda r: r.abort()); pb.route('**/css/skeleton.css', lambda r: r.abort())
    pb.add_init_script("window.__lcp=0;new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true})")
    pb.goto(url + '/index.html', wait_until='load'); pb.wait_for_timeout(2500)
    base = pb.evaluate("Math.round(window.__lcp)")
    check('4b LCP with skeleton ≤ LCP without + 150 ms (informational, local server)', perf['lcp'] <= base + 150, {'with': perf['lcp'], 'without': base})
    b.close()
json.dump(res, open(os.path.join(ROOT, 'docs', 'skel-results-6-1.json'), 'w'), indent=1)
print('OVERALL', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
