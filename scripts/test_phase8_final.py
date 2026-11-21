#!/usr/bin/env python3
"""Phase 8.6 final QA. Usage: python3 scripts/test_phase8_final.py [axe.min.js]   (axe-core is a dev tool, not shipped)"""
import asyncio, json, os, sys, threading, http.server, socketserver, functools
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AXE=sys.argv[1] if len(sys.argv)>1 else '/tmp/axe/node_modules/axe-core/axe.min.js'
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
S=socketserver.ThreadingTCPServer(('127.0.0.1',8795),functools.partial(H,directory=ROOT)); threading.Thread(target=S.serve_forever,daemon=True).start()
BASE='http://127.0.0.1:8795/index.html'; res=[]
def ck(n,ok,i=''):
    res.append((n,bool(ok),str(i))); print(('PASS ' if ok else 'FAIL ')+n,i)
W=[(320,640),(390,844),(768,1024),(1024,768),(1440,900)]
AX="async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes.length)}"
# every :hover rule must sit inside a (hover:hover) media block (previously completed mobile hover fix)
HOVER="""()=>{const bad=[];const walk=(rules,gated)=>{for(const r of rules){if(r.cssRules&&r.media){walk(r.cssRules,gated||/hover:\\s*hover|prefers-reduced-motion:\\s*reduce/.test(r.media.mediaText))}else if(r.cssRules&&r.selectorText===undefined){walk(r.cssRules,gated)}else if(r.selectorText&&/:hover/.test(r.selectorText)&&!gated)bad.push(r.selectorText.slice(0,70))}};
for(const ss of document.styleSheets){try{walk(ss.cssRules,false)}catch(e){}}return bad}"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for w,h in W:
        ctx=await b.new_context(viewport={'width':w,'height':h}); pg=await ctx.new_page(); errs=[]; reqs=[]
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:errs.append(m.text) if m.type in('error','warning') else None)
        pg.on('request',lambda r:reqs.append(r.url))
        await pg.add_init_script("window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:'layout-shift',buffered:true})")
        await pg.goto(BASE); await pg.wait_for_timeout(2200)
        Hh=await pg.evaluate('document.documentElement.scrollHeight')
        for y in range(0,Hh,400): await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(35)
        await pg.wait_for_timeout(2300)
        inl=await pg.evaluate("[...document.querySelectorAll('body *')].filter(e=>!e.matches('svg.icon')&&(e.style.opacity||e.style.visibility||e.style.transform)).length")
        ck(f'@{w} full scroll: overflow none, 0 leftover inline styles, 0 console warnings/errors, CLS<0.01, no external requests', not await pg.evaluate("document.documentElement.scrollWidth>innerWidth") and inl==0 and not errs and await pg.evaluate('window.__cls')<0.01 and not [r for r in reqs if not r.startswith('http://127.0.0.1')], {'inl':inl,'errs':errs[:2],'cls':await pg.evaluate('window.__cls')})
        ck(f'@{w} perf: 0 live ScrollTriggers after full scroll, 0 running animations at rest, no will-change', await pg.evaluate("ScrollTrigger.getAll().length")==0 and await pg.evaluate("document.getAnimations().filter(a=>a.playState==='running').length")==0 and await pg.evaluate("[...document.querySelectorAll('*')].filter(e=>getComputedStyle(e).willChange!=='auto').length")==0)
        await pg.add_script_tag(path=AXE); v=await pg.evaluate(AX); ck(f'@{w} axe (WCAG 2.2 AA + best practice) page: 0 violations', not v, v)
        if w in (390,1440):
            await pg.evaluate("document.querySelector('[data-event-open]').click()"); await pg.wait_for_timeout(600)
            v=await pg.evaluate(AX); ck(f'@{w} axe with event dialog open: 0 violations', not v, v); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500)
            await pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); await pg.wait_for_timeout(300)
            await pg.evaluate("document.querySelector('.gallery-card__action').click()"); await pg.wait_for_timeout(500)
            v=await pg.evaluate(AX); ck(f'@{w} axe with lightbox open: 0 violations', not v, v)
        await ctx.close()
    # regressions
    ctx=await b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True); pg=await ctx.new_page(); await pg.goto(BASE); await pg.wait_for_timeout(1500)
    ck('REGRESSION mobile hover fix: every :hover rule sits inside (hover:hover) and (pointer:fine) (or a reduced-motion block that cancels it)', not await pg.evaluate(HOVER), (await pg.evaluate(HOVER))[:4])
    ck('REGRESSION topbar logo: tap highlight suppressed, not global', await pg.evaluate("getComputedStyle(document.querySelector('.brand')).webkitTapHighlightColor")=='rgba(0, 0, 0, 0)' and await pg.evaluate("getComputedStyle(document.body).webkitTapHighlightColor")!='rgba(0, 0, 0, 0)')
    await pg.evaluate("document.querySelector('[data-event-open]').scrollIntoView({behavior:'instant',block:'center'})"); await pg.wait_for_timeout(1200)
    await pg.evaluate("document.querySelector('[data-event-open]').click()"); await pg.wait_for_timeout(500); await pg.evaluate("document.querySelector('.event-dialog__panel').scrollTop=500"); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500)
    await pg.evaluate("document.querySelector('[data-event-open]').click()"); await pg.wait_for_timeout(500)
    ck('REGRESSION event dialog resets internal scroll on every opening', await pg.evaluate("document.querySelector('.event-dialog__panel').scrollTop")==0); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(400)
    await pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); await pg.wait_for_timeout(300); await pg.evaluate("document.querySelector('.gallery-card__action').click()"); await pg.wait_for_timeout(500)
    hit=await pg.evaluate("['lightbox-prev','lightbox-next','lightbox-close'].map(id=>{const e=document.getElementById(id),r=e.getBoundingClientRect(),t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return t===e||e.contains(t)})")
    ck('REGRESSION lightbox floating prev/next/close layered and hit-testable (mobile)', all(hit), hit)
    await pg.focus('#lightbox-next'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200)
    ck('REGRESSION lightbox keyboard Next advances and stays open', await pg.evaluate("document.getElementById('memories-lightbox').open && document.getElementById('lightbox-counter').textContent")=='Photo 2 of 11')
    await ctx.close()
    # reduced motion: same content, no GSAP, no scroll smoothing
    ctx=await b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce'); pg=await ctx.new_page(); reqs=[]; pg.on('request',lambda r:reqs.append(r.url)); await pg.goto(BASE); await pg.wait_for_timeout(1500)
    ck('reduced motion: GSAP never requested, no pre-motion/js-motion, hero visible', not [r for r in reqs if 'gsap' in r.lower()] and await pg.evaluate("!document.documentElement.classList.contains('pre-motion')&&!document.documentElement.classList.contains('js-motion')&&+getComputedStyle(document.querySelector('.hero__title span')).opacity===1"))
    await ctx.close(); await b.close()
  bad=[r for r in res if not r[1]]
  print(f'\n{len(res)-len(bad)}/{len(res)} passed'); json.dump(res,open(os.path.join(ROOT,'docs','phase8-6-results.json'),'w'),indent=1); sys.exit(1 if bad else 0)
asyncio.run(main())
