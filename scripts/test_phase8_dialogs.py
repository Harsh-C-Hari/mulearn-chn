#!/usr/bin/env python3
"""Phase 8.4 tests: navigation, event dialogs, gallery + lightbox. Usage: python3 scripts/test_phase8_dialogs.py"""
import asyncio, json, os, sys, threading, http.server, socketserver, functools
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
S=socketserver.ThreadingTCPServer(('127.0.0.1',8772),functools.partial(H,directory=ROOT)); threading.Thread(target=S.serve_forever,daemon=True).start()
BASE='http://127.0.0.1:8772/index.html'; res=[]
def ck(n,ok,i=''):
    res.append((n,bool(ok),str(i))); print(('PASS ' if ok else 'FAIL ')+n,i)
W=[(320,640),(390,844),(768,1024),(1024,768),(1440,900)]
async def settle(pg):
    last=-1; st=0
    for _ in range(60):
        await pg.wait_for_timeout(100); y=await pg.evaluate('scrollY'); st=st+1 if y==last else 0; last=y
        if st>=3: break
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for w,h in W:
        touch=w<1024
        ctx=await b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch); pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
        await pg.goto(BASE); await pg.wait_for_timeout(1800)
        # ---- event dialog: 3 rapid open/close cycles, scroll reset every opening, focus restore, scroll lock, clean styles
        await pg.evaluate("document.querySelector('[data-event-open]').scrollIntoView({block:'center',behavior:'instant'})"); await pg.wait_for_timeout(1500)
        ok=True; info=[]
        for i in range(3):
            await pg.evaluate("document.querySelector('[data-event-open]').click()"); await pg.wait_for_timeout(120+i*100)
            await pg.evaluate("document.querySelector('.event-dialog__panel').scrollTop=400")
            await pg.keyboard.press('Escape'); await pg.wait_for_timeout(30+i*60)   # close while the open tween may still run
            await pg.wait_for_timeout(600)
            st=await pg.evaluate("(()=>{const d=document.getElementById('event-dialog'),p=d.querySelector('.event-dialog__panel');return {open:d.open,op:p.style.opacity,tr:p.style.transform,lock:getComputedStyle(document.body).overflow,focus:document.activeElement.hasAttribute('data-event-open')}})()")
            if st['open'] or st['op'] or st['tr'] or not st['focus'] or st['lock']=='hidden': ok=False
            info.append(st)
        ck(f'@{w} event dialog: rapid open/Esc ×3 leaves it closed, clean styles, focus on trigger, scroll unlocked',ok,info[-1])
        await pg.evaluate("document.querySelector('[data-event-open]').click()"); await pg.wait_for_timeout(700)
        ck(f'@{w} event dialog: reopened scrolled-to-top', await pg.evaluate("document.querySelector('.event-dialog__panel').scrollTop")==0)
        ck(f'@{w} event dialog: body scroll locked while open', await pg.evaluate("getComputedStyle(document.body).overflow")=='hidden')
        await pg.mouse.click(2,2) if not touch else await pg.evaluate("document.getElementById('event-dialog').dispatchEvent(new PointerEvent('pointerdown'));document.getElementById('event-dialog').click()")
        await pg.wait_for_timeout(700)
        ck(f'@{w} event dialog: backdrop closes', not await pg.evaluate("document.getElementById('event-dialog').open"))
        # ---- gallery + lightbox
        await pg.evaluate("document.getElementById('memories-gallery-toggle').scrollIntoView({block:'center',behavior:'instant'})"); await pg.wait_for_timeout(400)
        await pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); await settle(pg)
        await pg.click('.gallery-filter[data-filter="workshops"]'); await pg.wait_for_timeout(300)
        ck(f'@{w} filter announces result', 'Showing 4 photos in Workshops'==await pg.evaluate("document.getElementById('gallery-status').textContent"), await pg.evaluate("document.getElementById('gallery-status').textContent"))
        await pg.click('.gallery-filter[data-filter="all"]'); await pg.wait_for_timeout(200)
        trig=await pg.evaluate("(()=>{const b=document.querySelector('.gallery-card__action');b.focus();return b.closest('.gallery-card').dataset.id})()")
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(600)
        ck(f'@{w} lightbox opens by keyboard, focus on Close', await pg.evaluate("document.activeElement.id")=='lightbox-close')
        # nav controls on top of everything & hit-testable at their centre
        hit=await pg.evaluate("""(()=>{const out={};for(const id of ['lightbox-close','lightbox-prev','lightbox-next','lightbox-mob-prev','lightbox-mob-next']){const e=document.getElementById(id);const r=e.getBoundingClientRect();if(!r.width||getComputedStyle(e).visibility==='hidden'){out[id]='hidden';continue}const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);out[id]=(t===e||e.contains(t))}return out})()""")
        vis={k:v for k,v in hit.items() if v!='hidden'}
        ck(f'@{w} lightbox visible controls are hit-testable (layering)', vis and all(vis.values()), hit)
        # rapid navigation both ways, cyclic, state consistent
        for _ in range(23): await pg.keyboard.press('ArrowRight')
        await pg.keyboard.press('ArrowLeft'); await pg.wait_for_timeout(400)
        st=await pg.evaluate("(()=>{const c=document.getElementById('lightbox-counter').textContent;const n=+c.match(/Photo (\\d+)/)[1];const i=document.getElementById('lightbox-image');return {c,srcOk:i.src.includes(window.MULEARN.memories.gallery[n-1].src.replace(/^\\.?\\//,'')),loading:i.classList.contains('is-loading')}})()")
        await pg.wait_for_timeout(500)
        st2=await pg.evaluate("document.getElementById('lightbox-image').classList.contains('is-loading')")
        ck(f'@{w} lightbox: 24 rapid steps — image matches counter, loading state clears', st['srcOk'] and not st2, st)
        await pg.evaluate("document.querySelector('.lightbox-dialog__panel').scrollTop=300")
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(400)
        ck(f'@{w} lightbox: Esc closes and focus returns to the trigger', await pg.evaluate("document.activeElement.classList.contains('gallery-card__action')"))
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(500)
        ck(f'@{w} lightbox: reopened scrolled-to-top', await pg.evaluate("document.querySelector('.lightbox-dialog__panel').scrollTop")==0)
        ck(f'@{w} lightbox: page scroll locked', await pg.evaluate("getComputedStyle(document.body).overflow")=='hidden')
        await pg.click('#lightbox-close'); await pg.wait_for_timeout(300)
        ck(f'@{w} lightbox: Close button works', not await pg.evaluate("document.getElementById('memories-lightbox').open"))
        ck(f'@{w} no console errors / no overflow', not errs and not await pg.evaluate("document.documentElement.scrollWidth>innerWidth"), errs[:2])
        await ctx.close()
    # ---- navigation: mobile menu open/close paths + sticky header + anchor offset
    ctx=await b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True); pg=await ctx.new_page(); await pg.goto(BASE); await pg.wait_for_timeout(1500)
    nav="document.querySelector('[data-js=site-nav]').classList.contains('is-open')"
    await pg.tap('[data-js=menu-toggle]'); await pg.wait_for_timeout(400); a=await pg.evaluate(nav)
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200); bclose=not await pg.evaluate(nav)
    foc=await pg.evaluate("document.activeElement.matches('[data-js=menu-toggle]')")
    ck('nav 390: opens, Esc closes and returns focus',a and bclose and foc)
    await pg.tap('[data-js=menu-toggle]'); await pg.wait_for_timeout(300); await pg.tap('.site-nav a[href="#team"]'); await settle(pg)
    top=await pg.evaluate("Math.round(document.getElementById('team').getBoundingClientRect().top)")
    ck('nav 390: link tap closes menu and lands below header', not await pg.evaluate(nav) and 0<=top<=120, top)
    ck('nav 390: header stays sticky and shows is-stuck shadow', await pg.evaluate("document.querySelector('.site-header').getBoundingClientRect().top===0 && document.querySelector('.site-header').classList.contains('is-stuck')"))
    ck('nav 390: aria-current follows section', await pg.evaluate("(document.querySelector('.site-nav [aria-current]')||{}).textContent")=='Team')
    await pg.tap('[data-js=menu-toggle]'); await pg.wait_for_timeout(300); await pg.mouse.click(200,700); await pg.wait_for_timeout(300)
    ck('nav 390: tap outside closes menu', not await pg.evaluate(nav))
    await ctx.close(); await b.close()
  bad=[r for r in res if not r[1]]
  print(f'\n{len(res)-len(bad)}/{len(res)} passed'); json.dump(res,open(os.path.join(ROOT,'docs','phase8-4-results.json'),'w'),indent=1); sys.exit(1 if bad else 0)
asyncio.run(main())
