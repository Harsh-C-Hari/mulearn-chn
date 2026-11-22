#!/usr/bin/env python3
"""5.3 — accessibility, keyboard, motion, no-JS, forced-colours, failure and lightbox behaviour (held/failed/slow requests)."""
import sys, os, json, functools, time
sys.path.insert(0, os.path.dirname(__file__))
from skel_harness import *
from playwright.sync_api import sync_playwright
print = functools.partial(print, flush=True)
OUT = os.path.join(ROOT, 'docs', 'screenshots'); res = {}; ok = True
AXE = os.environ.get('AXE', '/tmp/axe/node_modules/axe-core/axe.min.js')
def check(n, c, i=''):
    global ok; ok = ok and bool(c); res[n] = {'pass': bool(c), 'info': str(i)[:400]}; print(('PASS ' if c else 'FAIL ') + n, str(i)[:260])
W5 = ((320, 700), (390, 844), (768, 1024), (1024, 768), (1440, 900))
FOCUSABLE = "a[href],button,input,select,textarea,[tabindex],summary,[contenteditable]"
srv, url = serve()
with sync_playwright() as p:
    b = p.chromium.launch()

    # ---- A. page-level a11y with skeletons showing ----
    pg = b.new_page(viewport={'width': 390, 'height': 844}); pg.set_default_timeout(10000); hold(pg)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1800)
    pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); pg.wait_for_timeout(400)
    n = pg.evaluate("document.querySelectorAll('.skel').length")
    check('A1 skeletons present for the a11y checks', n > 40, n)
    check('A2 every overlay aria-hidden=true, every inner svg aria-hidden, no title/desc/text', pg.evaluate("""[...document.querySelectorAll('.skel')].every(s=>s.getAttribute('aria-hidden')==='true'&&!s.querySelector('title,desc,text,foreignObject')&&s.textContent.trim()==='')"""))
    check('A3 nothing focusable inside an overlay, pointer-events none', pg.evaluate("""(F=>[...document.querySelectorAll('.skel')].every(s=>!s.matches(F)&&!s.querySelector(F)&&getComputedStyle(s).pointerEvents==='none'))(arguments[0])""".replace('arguments[0]', repr(FOCUSABLE))) if False else pg.evaluate("(F=>[...document.querySelectorAll('.skel')].every(s=>!s.matches(F)&&!s.querySelector(F)&&getComputedStyle(s).pointerEvents==='none'))", FOCUSABLE))
    check('A4 alt/src/width/height/loading untouched on skeleton hosts', pg.evaluate("""[...document.querySelectorAll('.skel')].every(s=>{const i=s.parentNode.querySelector('img');return i&&i.hasAttribute('alt')&&i.hasAttribute('width')&&i.hasAttribute('height')})"""))
    snap = pg.locator('body').aria_snapshot()
    check('A5 accessibility tree has no skeleton content', 'skel' not in snap.lower() and 'loading' not in snap.lower().replace('loading="lazy"', ''), len(snap))
    AXEJS = "axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}}).then(r=>r.violations.flatMap(v=>v.nodes.map(n=>v.id+'|'+n.target.join(' '))))"
    pg.add_script_tag(path=AXE); ax = set(pg.evaluate(AXEJS))
    pb = b.new_page(viewport={'width': 390, 'height': 844}); hold(pb); pb.route('**/js/skeleton.js', lambda r: r.abort())
    pb.goto(url + '/index.html', wait_until='domcontentloaded'); pb.wait_for_timeout(1800)
    pb.evaluate("document.getElementById('memories-gallery-toggle').click()"); pb.wait_for_timeout(400)
    pb.add_script_tag(path=AXE); base = set(pb.evaluate(AXEJS)); close_page(pb)
    check('A6 axe (WCAG 2.2 AA): skeletons add 0 violations vs. the same page without skeleton.js @390', ax <= base and not any('skel' in x for x in ax), {'with': len(ax), 'without': len(base), 'new': sorted(ax - base)[:4]})
    # tab order identical with and without skeletons (count of tab stops, none inside overlays)
    stops = 0; inside = 0
    pg.evaluate("document.body.focus()")
    for _ in range(80):
        pg.keyboard.press('Tab')
        r = pg.evaluate("(()=>{const a=document.activeElement;return {t:a===document.body,s:!!(a&&a.closest&&a.closest('.skel'))}})()")
        if r['t']: break
        stops += 1; inside += r['s']
    check('A7 keyboard tab walk never lands in an overlay', inside == 0 and stops > 10, {'stops': stops, 'inside': inside})
    close_page(pg)

    # ---- B. reduced motion at every width ----
    for w, h in W5:
        ctx = b.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce'); pg = ctx.new_page(); pg.set_default_timeout(10000); hold(pg)
        pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1500)
        pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); pg.wait_for_timeout(300)
        running = pg.evaluate("document.getAnimations().filter(a=>a.effect&&a.effect.target&&a.effect.target.closest&&a.effect.target.closest('.skel')).length")
        check(f'B {w}: reduced motion → 0 running skeleton animations', running == 0, running)
        close_page(pg); ctx.close()
    # motion on: only decorative marks move (and only small ones)
    pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.set_default_timeout(10000); hold(pg)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1500)
    big = pg.evaluate("""[...document.getAnimations()].filter(a=>a.effect&&a.effect.target&&a.effect.target.closest&&a.effect.target.closest('.skel')).filter(a=>{const r=a.effect.target.getBoundingClientRect();return r.width*r.height>10000}).length""")
    check('B6 motion on: no animated element larger than 100x100 px (area)', big == 0, big)
    ms = pg.evaluate("[...document.getAnimations()].filter(a=>a.effect&&a.effect.target&&a.effect.target.closest&&a.effect.target.closest('.skel')).map(a=>a.effect.getTiming().duration)")
    check('B7 motion on: only ≥1.8s calm loops (no fast flashing)', ms and min(ms) >= 1800, [min(ms), max(ms)] if ms else ms)
    close_page(pg)

    # ---- C. no-JS and script-blocked ----
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, java_script_enabled=False); pg = ctx.new_page()
    pg.goto(url + '/index.html', wait_until='load'); pg.wait_for_timeout(800)
    imgs = pg.evaluate("[...document.querySelectorAll('img:not([loading=lazy])')].filter(i=>i.getAttribute('src')&&i.getBoundingClientRect().width>0).map(i=>i.complete&&i.naturalWidth>0)")
    check('C1 JS off: no overlay ever exists, eager images render normally', pg.evaluate("document.querySelectorAll('.skel').length")==0 and imgs and all(imgs), len(imgs))
    check('C2 JS off: no attribute residue on hosts', pg.evaluate("document.querySelectorAll('[data-skel-state]').length")==0)
    ctx.close()
    ctx = b.new_context(viewport={'width': 390, 'height': 844}); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.route('**/js/skeleton.js', lambda r: r.abort())
    pg.goto(url + '/index.html', wait_until='load'); pg.wait_for_timeout(1200)
    check('C3 skeleton.js blocked: page works, 0 overlays, 0 page errors', pg.evaluate("document.querySelectorAll('.skel').length")==0 and not errs, errs)
    ctx.close()

    # ---- D. forced colours (Windows high contrast) ----
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, forced_colors='active'); pg = ctx.new_page(); pg.set_default_timeout(10000); hold(pg)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1500)
    pg.evaluate("document.querySelector('.skel--poster').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
    vis = pg.evaluate("""[...document.querySelectorAll('.skel--poster,.skel--about,.skel--portrait')].map(s=>{const c=getComputedStyle(s);return {k:s.className.split(' ')[1],bw:c.borderTopWidth,st:c.borderTopStyle,col:c.borderTopColor}})""")
    check('D1 forced colours: bordered overlays keep a solid system-colour border', all(v['st'] == 'solid' and v['bw'] != '0px' for v in vis), vis[:3])
    pg.screenshot(path=os.path.join(OUT, 'skel-5-3-forced-colors-1440.png')); close_page(pg); ctx.close()

    # ---- E. failed images: static, no endless loader, alt kept ----
    pg = b.new_page(viewport={'width': 390, 'height': 844}); pg.set_default_timeout(10000); fail(pg)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(2500)
    pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelectorAll('[loading=lazy]').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(1500)
    st = pg.evaluate("""(()=>{const s=[...document.querySelectorAll('.skel')];return {n:s.length,failed:s.filter(x=>x.classList.contains('is-failed')).length,anim:document.getAnimations().filter(a=>a.effect&&a.effect.target&&a.effect.target.closest&&a.effect.target.closest('.skel')).length,ico:s.filter(x=>x.querySelector('.skel__ico')).length}})()""")
    check('E1 every failed image shows the static failed state (no loading overlays left)', st['n'] > 40 and st['n'] == st['failed'] == st['ico'], st)
    check('E2 failed state has 0 running animations', st['anim'] == 0, st)
    n1 = pg.evaluate("document.querySelectorAll('.skel').length"); pg.wait_for_timeout(1500); n2 = pg.evaluate("document.querySelectorAll('.skel').length")
    check('E3 failure state is stable (no retry/flicker loop)', n1 == n2, (n1, n2))
    check('E4 failed icon is hidden from AT; alt untouched', pg.evaluate("[...document.querySelectorAll('.skel.is-failed')].every(s=>s.getAttribute('aria-hidden')==='true'&&s.parentNode.querySelector('img').hasAttribute('alt'))"))
    pg.evaluate("document.querySelector('.skel--poster').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(OUT, 'skel-5-3-failed-390.png')); close_page(pg)

    # ---- F. slow request → skeleton → image, skeleton never delays the image ----
    pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.set_default_timeout(15000); hold(pg)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1500)
    check('F1 hero skeleton visible while its bytes are pending', pg.evaluate("!!document.querySelector('.hero__figure .skel--hero')"))
    t0 = time.time(); release(pg); pg.unroute_all(behavior='ignore_errors')
    pg.wait_for_function("!document.querySelector('.hero__figure .skel--hero')", timeout=8000); dt = time.time() - t0
    gone = pg.evaluate("(()=>{const i=document.querySelector('.hero__figure img');return i.complete&&i.naturalWidth>0})()")
    check('F2 skeleton removed once the image has loaded; image complete', gone, round(dt, 2))
    close_page(pg)

    # ---- G. cached images: skeleton never created for already-complete images ----
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}); pg = ctx.new_page(); pg.set_default_timeout(15000)
    pg.goto(url + '/index.html', wait_until='load'); pg.wait_for_timeout(2500)
    pg.close(); pg = ctx.new_page(); pg.set_default_timeout(15000)
    pg.add_init_script("""window.__skelBorn=[];window.__skelBornVisible=[];new MutationObserver(r=>{r.forEach(x=>x.addedNodes.forEach(n=>{if(n.classList&&n.classList.contains('skel')){window.__skelBorn.push(n.className);const q=n.getBoundingClientRect();if(q.width>0&&q.bottom>0&&q.top<innerHeight)window.__skelBornVisible.push(n.className)}}))}).observe(document,{childList:true,subtree:true})""")
    pg.goto(url + '/index.html', wait_until='load'); pg.wait_for_timeout(2000)
    born = pg.evaluate("window.__skelBorn")
    inview = pg.evaluate("[...document.querySelectorAll('.skel')].filter(s=>{const r=s.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight&&r.width>0}).length")
    check('G1 second visit (cache warm): no skeleton ever created for in-viewport images, none visible after load', pg.evaluate("window.__skelBornVisible.length") == 0 and inview == 0, {'visible_born': pg.evaluate("window.__skelBornVisible"), 'inview': inview, 'offscreen_lazy_overlays': len(born)})
    pg.evaluate("document.querySelector('[data-lightbox-open]').click()"); pg.wait_for_timeout(600)
    pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(300); pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(600)
    check('G2 lightbox: a photo already loaded (back to previous) shows no skeleton', pg.evaluate("document.querySelectorAll('.skel--lightbox').length") == 0)
    ctx.close()

    # ---- H. lightbox at five widths, held requests ----
    for w, h in W5:
        pg = b.new_page(viewport={'width': w, 'height': h}); pg.set_default_timeout(10000); hold(pg)
        pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1200)
        trig = pg.locator('[data-lightbox-open]').first; trig.scroll_into_view_if_needed(); trig.focus(); pg.keyboard.press('Enter'); pg.wait_for_timeout(500)
        g = pg.evaluate("""(()=>{const s=document.querySelector('.skel--lightbox'),st=document.querySelector('.lightbox-dialog__stage'),pn=document.querySelector('.lightbox-dialog__panel')||document.querySelector('#lightbox-dialog');
          if(!s)return null;const a=s.getBoundingClientRect(),b=st.getBoundingClientRect(),i=document.getElementById('lightbox-image');
          const ar=parseFloat(getComputedStyle(s).getPropertyValue('--skel-ar')||s.parentNode.style.getPropertyValue('--skel-ar'))||0;
          return {w:a.width,h:a.height,sw:b.width,ar:+(a.width/a.height).toFixed(3),iw:+i.getAttribute('width'),ih:+i.getAttribute('height'),vh:innerHeight,over:document.documentElement.scrollWidth-document.documentElement.clientWidth,imgHidden:getComputedStyle(i).display==='none'}})()""")
        want = g and round(g['iw'] / g['ih'], 3)
        check(f'H {w}: lightbox skeleton ratio == photo ratio, within stage, ≤58vh, image hidden meanwhile', g and abs(g['ar'] - want) < 0.02 and g['w'] <= g['sw'] + 1 and g['h'] <= g['vh'] * .58 + 1 and g['imgHidden'], g)
        check(f'H {w}: no horizontal overflow with lightbox skeleton', g and g['over'] <= 0, g and g['over'])
        # controls stay reachable & functional while the skeleton is showing
        hit = pg.evaluate("""['lightbox-prev','lightbox-next','lightbox-mob-prev','lightbox-mob-next'].map(id=>{const e=document.getElementById(id),r=e.getBoundingClientRect();if(!r.width)return null;const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return e.contains(t)})""")
        check(f'H {w}: visible prev/next controls are the top element (not covered by the skeleton)', [x for x in hit if x is not None] and all(x for x in hit if x is not None), hit)
        # rapid navigation with all requests still pending, then release
        a0 = pg.evaluate("document.getElementById('lightbox-image').alt")
        for _ in range(3): pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(120)
        mid = pg.evaluate("({n:document.querySelectorAll('.skel--lightbox').length,alt:document.getElementById('lightbox-image').alt,title:document.getElementById('lightbox-title').textContent,counter:document.getElementById('lightbox-counter')&&document.getElementById('lightbox-counter').textContent})")
        check(f'H {w}: rapid next ×3 while pending → exactly one skeleton, caption == new alt', mid['n'] == 1 and mid['alt'] == mid['title'] and mid['alt'] != a0, mid)
        release(pg); pg.unroute_all(behavior='ignore_errors'); pg.wait_for_timeout(2000)
        fin = pg.evaluate("(()=>{const i=document.getElementById('lightbox-image');return {n:document.querySelectorAll('.skel--lightbox').length,ok:i.complete&&i.naturalWidth>0,alt:i.alt,title:document.getElementById('lightbox-title').textContent,state:document.querySelector('.lightbox-dialog__stage').getAttribute('data-skel-state')}})()")
        check(f'H {w}: after release the last photo shows, no skeleton, no stuck state', fin['n'] == 0 and fin['ok'] and fin['alt'] == fin['title'] and fin['state'] is None, fin)
        if w in (390, 1440):
            pg.screenshot(path=os.path.join(OUT, f'skel-5-3-lightbox-{w}.png'))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        check(f'H {w}: Esc closes the lightbox and returns focus to its trigger', pg.evaluate("!document.getElementById('memories-lightbox').open") and pg.evaluate("!!document.activeElement.closest('[data-lightbox-open]')"), pg.evaluate("document.activeElement.className"))
        close_page(pg)

    # ---- I. lightbox + axe with skeleton showing ----
    pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.set_default_timeout(10000); hold(pg)
    pg.goto(url + '/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1200)
    pg.evaluate("document.querySelector('[data-lightbox-open]').click()"); pg.wait_for_timeout(500)
    pg.add_script_tag(path=AXE)
    ax = pg.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))")
    check('I1 axe 0 violations with the lightbox skeleton showing @1440', ax == [], ax)
    close_page(pg)
    b.close()
json.dump(res, open(os.path.join(ROOT, 'docs', 'skel-results-5-3.json'), 'w'), indent=1)
print('OVERALL', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
