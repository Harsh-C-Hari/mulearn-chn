#!/usr/bin/env python3
"""5.1 — board-mix visual pass: coverage, forbidden effects, host-colour echo, motion on/off, lightbox look."""
import sys, os, json, re, functools
sys.path.insert(0, os.path.dirname(__file__))
from skel_harness import *
from playwright.sync_api import sync_playwright
print = functools.partial(print, flush=True)
OUT = os.path.join(ROOT, 'docs', 'screenshots'); res = {}; ok = True
def check(n, c, i=''):
    global ok; ok = ok and bool(c); res[n] = {'pass': bool(c), 'info': str(i)[:300]}; print(('PASS ' if c else 'FAIL ') + n, str(i)[:200])

src = open(os.path.join(ROOT, 'css/skeleton.css')).read() + open(os.path.join(ROOT, 'js/skeleton.js')).read()
check('no gradient/blur/drop-shadow/filter in skeleton css+js', not re.search(r'gradient\(|blur\(|drop-shadow|filter\s*:', src))
check('only the two documented new hex values (+ none else)', sorted(set(re.findall(r'#[0-9A-Fa-f]{6}\b', open(os.path.join(ROOT, 'css/skeleton.css')).read()))) == ['#E4DAC3', '#F1EADA'],
      set(re.findall(r'#[0-9A-Fa-f]{6}\b', open(os.path.join(ROOT, 'css/skeleton.css')).read())))

srv, url = serve()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.set_default_timeout(8000); hold(pg)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1500)
    cnt = pg.evaluate("""()=>{const o={};document.querySelectorAll('.skel').forEach(s=>{const k=[...s.classList].find(c=>c.startsWith('skel--'));o[k]=(o[k]||0)+1});return o}""")
    exp = {'skel--hero': 1, 'skel--about': 1, 'skel--poster': 3, 'skel--mini': 4, 'skel--portrait': 4, 'skel--roster': 21, 'skel--gallery': 11}
    check('coverage counts (held)', all(cnt.get(k) == v for k, v in exp.items()) and cnt.get('skel--collage', 0) + cnt.get('skel--collage-sq', 0) == 6, cnt)
    check('every overlay aria-hidden', pg.evaluate("[...document.querySelectorAll('.skel')].every(s=>s.getAttribute('aria-hidden')==='true')"))
    fills = pg.evaluate("[...document.querySelectorAll('.member-card__photo .skel .tn')].map(e=>getComputedStyle(e).fill)")
    check('portrait tint == each card colour (yellow/indigo/mint/yellow)', fills == ['rgb(250, 204, 21)', 'rgb(99, 102, 241)', 'rgb(52, 211, 153)', 'rgb(250, 204, 21)'], fills)
    rr = pg.evaluate("[...document.querySelectorAll('.roster__photo')].slice(0,8).map(f=>[getComputedStyle(f).backgroundColor,getComputedStyle(f.querySelector('.skel .tn')).fill])")
    check('roster tint == its own mat colour', all(a == c for a, c in rr), rr)
    pf = pg.evaluate("[...document.querySelectorAll('.event-card__poster .skel .tn3')].map(e=>getComputedStyle(e).fill)")
    check('poster field echoes card colour', pf == ['rgb(251, 143, 124)', 'rgb(79, 70, 229)', 'rgb(250, 204, 21)'], pf)
    anim = pg.evaluate("""()=>({w:[...document.querySelectorAll('.skel [data-w]')].map(e=>getComputedStyle(e).animationName).filter((v,i,a)=>a.indexOf(v)===i),
         a:[...document.querySelectorAll('.skel--poster [data-a]')].map(e=>getComputedStyle(e).animationName).filter((v,i,a)=>a.indexOf(v)===i),
         mini:[...document.querySelectorAll('.skel--mini [data-w],.skel--roster [data-a]')].map(e=>getComputedStyle(e).animationName)})""")
    check('motion on: stickers tilt, accents breathe, mini/roster static', anim['w'] == ['skel-tilt'] and anim['a'] == ['skel-breathe'] and set(anim['mini']) <= {'none'}, anim)
    big = pg.evaluate("[...document.querySelectorAll('.skel > svg > rect.sh, .skel > svg > rect.tn, .skel > svg > rect.tn2')].every(e=>getComputedStyle(e).animationName==='none')")
    check('large surfaces never animate', big)
    close_page(pg)
    # reduced motion
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce'); pg = ctx.new_page(); pg.set_default_timeout(8000); hold(pg)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1200)
    rm = pg.evaluate("[...document.querySelectorAll('.skel [data-w],.skel [data-a]')].map(e=>getComputedStyle(e).animationName).filter((v,i,a)=>a.indexOf(v)===i)")
    check('reduced motion: all skeleton animation off', rm == ['none'], rm); close_page(pg); ctx.close()
    # lightbox looks (desktop + mobile, landscape + portrait photo)
    for w, h, tag in ((1440, 900, '1440'), (390, 844, '390')):
        pg = b.new_page(viewport={'width': w, 'height': h}); pg.set_default_timeout(8000); hold(pg)
        pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1000)
        pg.evaluate("document.querySelector('[data-lightbox-open]').click()"); pg.wait_for_timeout(500)
        st = pg.evaluate("(()=>{const s=document.querySelector('.skel--lightbox');return s?{w:s.getBoundingClientRect().width,h:s.getBoundingClientRect().height}:null})()")
        check(f'lightbox skeleton present @{tag}', st and st['w'] > 100, st)
        pg.screenshot(path=os.path.join(OUT, f'skel-5-1-lightbox-{tag}.png')); close_page(pg)
    b.close()
json.dump(res, open(os.path.join(ROOT, 'docs', 'skel-results-5-1.json'), 'w'), indent=1)
print('OVERALL', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
