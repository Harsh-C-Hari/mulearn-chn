#!/usr/bin/env python3
"""5.4 — visual review captures: each skeleton section at 390 and 1440 with all image requests held."""
import sys, os, functools
sys.path.insert(0, os.path.dirname(__file__))
from skel_harness import *
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'screenshots'); srv, url = serve()
SECS = {'hero': '.hero', 'about': '#about', 'team': '#team', 'memories': '#memories'}
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in ((390, 844), (1440, 900)):
        pg = b.new_page(viewport={'width': w, 'height': h}); pg.set_default_timeout(10000); hold(pg)
        pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1500)
        pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); pg.wait_for_timeout(300)
        pg.evaluate("document.querySelectorAll('[loading=lazy]').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(500)
        for name, sel in SECS.items():
            pg.evaluate("s=>{const e=document.querySelector(s);e.scrollIntoView();document.querySelectorAll('[data-motion],.is-hidden').forEach(x=>{x.style.opacity=1;x.style.transform='none'})}", sel); pg.wait_for_timeout(350)
            pg.locator(sel).first.screenshot(path=os.path.join(OUT, f'skel-5-4-{name}-{w}.png'))
        close_page(pg)
    b.close()
