#!/usr/bin/env python3
"""4.7 — event-dialog photo skeletons: slow / failed / normal / re-open / no-poster-skeleton / geometry."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from skel_harness import *
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'screenshots'); os.makedirs(OUT, exist_ok=True)
res = {}; ok = True
def check(name, cond, info=''):
    global ok; ok = ok and bool(cond); res[name] = {'pass': bool(cond), 'info': info}
    print(('PASS ' if cond else 'FAIL ') + name, info)

GEO = '''() => [...document.querySelectorAll('.event-dialog__photo')].map(f => {
  const i=f.querySelector('img'), s=f.querySelector('.skel'); if(!s) return null;
  const a=i.getBoundingClientRect(), b=s.getBoundingClientRect();
  return {dx:Math.abs(a.left-b.left),dy:Math.abs(a.top-b.top),dw:Math.abs(a.width-b.width),dh:Math.abs(a.height-b.height),
          hidden:s.getAttribute('aria-hidden'), pe:getComputedStyle(s).pointerEvents, alt:i.alt.length>0}})'''
srv, url = serve()
with sync_playwright() as p:
    b = p.chromium.launch()
    # 1 · slow (held) -----------------------------------------------------------
    pg = b.new_page(viewport={'width': 1280, 'height': 900}); hold(pg)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(600)
    pg.click('[data-event-open="odyssey"]', force=True); pg.wait_for_timeout(500)
    g = pg.evaluate(GEO)
    check('slow: one skeleton per photo (odyssey=2)', len(g) == 2 and all(g), g)
    check('slow: skeleton box == image box (<=1px)', all(x and max(x['dx'], x['dy'], x['dw'], x['dh']) <= 1 for x in g), g)
    check('slow: aria-hidden + pointer-events none + alt kept', all(x['hidden'] == 'true' and x['pe'] == 'none' and x['alt'] for x in g))
    check('slow: poster has NO skeleton', pg.evaluate("document.querySelectorAll('.event-dialog__poster .skel').length") == 0)
    pg.screenshot(path=os.path.join(OUT, 'skel-4-7-dialog-loading-1280.png'))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
    pg.click('[data-event-open="odyssey"]', force=True); pg.wait_for_timeout(400)
    check('re-open: still exactly 2 skeletons (no duplicates)', pg.evaluate("document.querySelectorAll('.event-dialog .skel').length") == 2)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
    pg.click('[data-event-open="techforge"]', force=True); pg.wait_for_timeout(400)
    check('event without photos: no skeleton, no error', pg.evaluate("document.querySelectorAll('.event-dialog .skel').length") == 0)
    close_page(pg)
    # 2 · normal -------------------------------------------------------------------
    pg = b.new_page(viewport={'width': 1280, 'height': 900}); errs = []
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto(url + '/index.html'); pg.wait_for_timeout(500)
    pg.click('[data-event-open="buildathon"]', force=True); pg.wait_for_timeout(1200)
    check('normal: skeleton removed after load', pg.evaluate("document.querySelectorAll('.event-dialog .skel').length") == 0)
    check('normal: no data-skel-state left on figure', pg.evaluate("document.querySelectorAll('.event-dialog [data-skel-state]').length") == 0)
    check('normal: photo really loaded', pg.evaluate("[...document.querySelectorAll('.event-dialog__photo img')].every(i=>i.complete&&i.naturalWidth>0)"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
    pg.click('[data-event-open="odyssey"]', force=True); pg.wait_for_timeout(300)
    check('cached/re-render: no skeleton for already-loaded photos', pg.evaluate("document.querySelectorAll('.event-dialog .skel').length") == 0)
    check('no console errors', not errs, errs); pg.close()
    # 3 · failed -------------------------------------------------------------------
    pg = b.new_page(viewport={'width': 1280, 'height': 900}); fail(pg)
    pg.goto(url + '/index.html'); pg.wait_for_timeout(500)
    pg.click('[data-event-open="odyssey"]', force=True); pg.wait_for_timeout(600)
    st = pg.evaluate("[...document.querySelectorAll('.event-dialog .skel')].map(s=>({f:s.classList.contains('is-failed'),anim:[...s.querySelectorAll('[data-a]')].length}))")
    check('failed: static failed overlay (not an endless loader)', len(st) == 2 and all(x['f'] for x in st), st)
    pg.screenshot(path=os.path.join(OUT, 'skel-4-7-dialog-failed-1280.png'))
    pg.close()
    # 4 · mobile geometry ----------------------------------------------------------
    pg = b.new_page(viewport={'width': 320, 'height': 700}); hold(pg)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(600)
    pg.click('[data-event-open="useless"]', force=True); pg.wait_for_timeout(500)
    g = pg.evaluate(GEO)
    check('320px: skeleton == image box', len(g) == 1 and g[0] and max(g[0]['dx'], g[0]['dy'], g[0]['dw'], g[0]['dh']) <= 1, g)
    check('320px: no horizontal overflow in dialog', pg.evaluate("(()=>{const d=document.querySelector('.event-dialog__panel');return d.scrollWidth<=d.clientWidth+1})()"))
    pg.screenshot(path=os.path.join(OUT, 'skel-4-7-dialog-loading-320.png'))
    close_page(pg); b.close()
json.dump(res, open(os.path.join(ROOT, 'docs', 'skel-results-4-7.json'), 'w'), indent=1)
print('\nOVERALL', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
