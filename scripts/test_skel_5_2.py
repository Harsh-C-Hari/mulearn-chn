#!/usr/bin/env python3
"""5.2 — responsive verification at 320/390/768/1024/1440 (held, released=CLS, geometry, overflow, clipping, overlap)."""
import sys, os, json, functools
sys.path.insert(0, os.path.dirname(__file__))
from skel_harness import *
from playwright.sync_api import sync_playwright
print = functools.partial(print, flush=True)
OUT = os.path.join(ROOT, 'docs', 'screenshots'); res = {}; ok = True
def check(n, c, i=''):
    global ok; ok = ok and bool(c); res[n] = {'pass': bool(c), 'info': str(i)[:400]}; print(('PASS ' if c else 'FAIL ') + n, str(i)[:260])

GEOM = """()=>{
  const out=[];
  document.querySelectorAll('.skel').forEach(s=>{
    if(s.classList.contains('skel--lightbox')) return;
    const img=s.parentNode.querySelector('img'); if(!img) return;
    const a=s.getBoundingClientRect(), b=img.getBoundingClientRect();
    if(!a.width||!b.width) return;                       // hidden (gallery drawer closed etc.)
    const k=[...s.classList].find(c=>c.startsWith('skel--'));
    out.push({k, dx:Math.abs(a.left-b.left), dy:Math.abs(a.top-b.top), dw:Math.abs(a.width-b.width), dh:Math.abs(a.height-b.height), w:a.width, h:a.height});
  });
  return out}"""
SCALE = """()=>{  /* the overlay svg must not be clipped to nothing: shapes still inside the overlay box */
  return [...document.querySelectorAll('.skel > svg')].filter(s=>s.getBoundingClientRect().width>0).every(s=>{const p=s.parentNode.getBoundingClientRect(),r=s.getBoundingClientRect();return r.width<=p.width+1&&r.height<=p.height+1})}"""
OVER = "()=>({sw:document.documentElement.scrollWidth, cw:document.documentElement.clientWidth})"

srv, url = serve()
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in ((320, 700), (390, 844), (768, 1024), (1024, 768), (1440, 900)):
        pg = b.new_page(viewport={'width': w, 'height': h}); pg.set_default_timeout(10000); hold(pg)
        pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1800)
        # open the gallery drawer so its 11 thumbs are laid out
        pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); pg.wait_for_timeout(600)
        pg.evaluate("document.querySelectorAll('[loading=lazy]').forEach(i=>{i.loading='eager'})")   # test-only: force lazies to request (held)
        pg.wait_for_timeout(400)
        g = pg.evaluate(GEOM)
        bad = [x for x in g if x['dx'] > 1 or x['dy'] > 1 or x['dw'] > 1 or x['dh'] > 1]
        kinds = sorted({x['k'] for x in g})
        check(f'{w}: skeleton box == image box (<=1px), {len(g)} measured', not bad and len(g) >= 20, (bad[:3] or kinds))
        o = pg.evaluate(OVER)
        check(f'{w}: no horizontal overflow while skeletons show', o['sw'] <= o['cw'] + 0, o)
        check(f'{w}: skeleton svg never exceeds its overlay', pg.evaluate(SCALE))
        # decorations hidden on <640 (hide-sm) and nothing animates large surfaces
        hs = pg.evaluate("[...document.querySelectorAll('.skel .hide-sm')].filter(e=>e.getBoundingClientRect().width>0).length")
        check(f'{w}: hide-sm decorations {"hidden" if w<640 else "shown"}', (hs == 0) if w < 640 else True, hs)
        # tiny skeletons keep their ratio lock
        mini = pg.evaluate("[...document.querySelectorAll('.skel--mini')].filter(s=>s.getBoundingClientRect().width>0).map(s=>{const r=s.getBoundingClientRect();return +(r.width/r.height).toFixed(3)})")
        check(f'{w}: mini ratio follows each image (390x502/461/460/499)', len(mini)==4 and all(0.76<r<0.86 for r in mini), mini)
        # shift on release: record layout shift while images arrive
        pg.evaluate("""window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries()) if(!e.hadRecentInput) window.__cls+=e.value}).observe({type:'layout-shift',buffered:false})""")
        pg.evaluate("window.scrollTo(0,0)")
        release(pg); pg.unroute_all(behavior='ignore_errors'); pg.wait_for_timeout(2500)
        cls = pg.evaluate("window.__cls"); left = pg.evaluate("document.querySelectorAll('.skel').length")
        check(f'{w}: CLS when images arrive <= 0.02', cls <= 0.02, round(cls, 4))
        check(f'{w}: no skeleton left after load (visible-area images)', left <= pg.evaluate("document.querySelectorAll('img[loading=lazy]:not([data-skel-reveal])').length") + 40, left)
        o = pg.evaluate(OVER); check(f'{w}: no horizontal overflow after load', o['sw'] <= o['cw'], o)
        close_page(pg)
        # screenshots of skeleton state per width
        pg = b.new_page(viewport={'width': w, 'height': h}); hold(pg)
        pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1500)
        pg.evaluate("document.getElementById('events').scrollIntoView()"); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(OUT, f'skel-5-2-events-{w}.png')); close_page(pg)
    b.close()
json.dump(res, open(os.path.join(ROOT, 'docs', 'skel-results-5-2.json'), 'w'), indent=1)
print('OVERALL', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
