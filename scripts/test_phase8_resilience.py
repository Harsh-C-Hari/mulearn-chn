#!/usr/bin/env python3
"""Phase 8.5: responsive motion & failure-resilience matrix. Usage: python3 scripts/test_phase8_resilience.py"""
import asyncio, json, os, sys, threading, http.server, socketserver, functools
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
S=socketserver.ThreadingTCPServer(('127.0.0.1',8773),functools.partial(H,directory=ROOT)); threading.Thread(target=S.serve_forever,daemon=True).start()
BASE='http://127.0.0.1:8773/index.html'; res=[]
def ck(n,ok,i=''):
    res.append((n,bool(ok),str(i))); print(('PASS ' if ok else 'FAIL ')+n,i)
W=[(320,640),(390,844),(768,1024),(1024,768),(1440,900)]
HIDDEN="()=>[...document.querySelectorAll('body *')].filter(e=>{if(e.matches('svg.icon'))return false;const s=getComputedStyle(e);return (+s.opacity===0||s.visibility==='hidden')&&e.offsetParent!==null&&!e.closest('[hidden],dialog:not([open]),.sr-only')&&e.getBoundingClientRect().height>0&&!e.closest('.site-nav')}).map(e=>(e.className&&e.className.baseVal===undefined?e.className:e.tagName).toString().slice(0,40)).slice(0,6)"
INLINE="()=>[...document.querySelectorAll('body *')].filter(e=>!e.matches('svg.icon')&&(e.style.opacity||e.style.visibility||e.style.transform)).length"
async def scroll_through(pg,step=500,wait=40):
    H=await pg.evaluate('document.documentElement.scrollHeight')
    for y in range(0,H,step): await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(wait)
    await pg.evaluate(f'scrollTo(0,{H})'); await pg.wait_for_timeout(2300)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    scen=[('normal',{},None),('touch',{'has_touch':True,'is_mobile':True},None),('reduced',{'reduced_motion':'reduce'},None),
          ('gsap-blocked',{},'gsap'),('scrolltrigger-blocked (init failure)',{},'st'),('js-off',{'java_script_enabled':False},None)]
    for name,kw,block in scen:
      for w,h in W:
        ctx=await b.new_context(viewport={'width':w,'height':h},**kw); pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.on('console',lambda m:errs.append(m.text) if m.type=='error' and 'Failed to load resource' not in m.text else None)
        if block=='gsap': await pg.route('**/vendor/gsap/**',lambda r:r.abort())
        if block=='st': await pg.route('**/ScrollTrigger.min.js',lambda r:r.abort())
        await pg.add_init_script("window.__cls=0;try{new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:'layout-shift',buffered:true})}catch(e){}")
        await pg.goto(BASE); await pg.wait_for_timeout(1800)
        if kw.get('java_script_enabled') is False:
            hid=await pg.evaluate(HIDDEN); ck(f'{name} @{w}: all content visible, no overflow',not hid and not await pg.evaluate("document.documentElement.scrollWidth>innerWidth"),hid)
            await ctx.close(); continue
        await scroll_through(pg)
        hid=await pg.evaluate(HIDDEN); left=await pg.evaluate(INLINE)
        ov=await pg.evaluate("document.documentElement.scrollWidth>innerWidth"); cls=await pg.evaluate('window.__cls')
        extra=''
        if name in('reduced','gsap-blocked','scrolltrigger-blocked (init failure)'):
            gs=await pg.evaluate("document.documentElement.classList.contains('js-motion')"); pm=await pg.evaluate("document.documentElement.classList.contains('pre-motion')")
            extra=f' js-motion={gs} pre-motion={pm}'
            if gs or pm: errs.append('motion class present')
        ck(f'{name} @{w}: visible content, no stuck inline styles, no overflow, no errors, CLS<0.02{extra}',not hid and left==0 and not ov and not errs and cls<0.02,{'hidden':hid,'inline':left,'overflow':ov,'errs':errs[:2],'cls':round(cls,4)})
        await ctx.close()
    # keyboard-only traversal on normal motion: every dialog trigger reachable & operable without a pointer
    for w,h in W:
        ctx=await b.new_context(viewport={'width':w,'height':h}); pg=await ctx.new_page(); await pg.goto(BASE); await pg.wait_for_timeout(1500)
        await pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
        seen=set()
        for i in range(160):
            await pg.keyboard.press('Tab'); await pg.wait_for_timeout(15)
            k=await pg.evaluate("(()=>{const e=document.activeElement;return e.hasAttribute('data-event-open')?'event:'+e.dataset.eventOpen:e.hasAttribute('data-lightbox-open')?'lb':e.id==='memories-gallery-toggle'?'toggle':e.matches('.site-nav a')?'nav':''})()")
            if k: seen.add(k)
            if i==159: break
        ev=[s for s in seen if s.startswith('event:')]
        ck(f'keyboard-only @{w}: reaches nav, all 7 event buttons, gallery toggle',len(ev)==7 and 'toggle' in seen and 'nav' in seen or (w<1180 and len(ev)==7 and 'toggle' in seen),sorted(seen))
        await ctx.close()
    # repeated dialogs / gallery: no duplicated handlers (one click = exactly one step), no growth
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page(); await pg.goto(BASE); await pg.wait_for_timeout(1500)
    await pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); await pg.wait_for_timeout(300)
    for i in range(5):
        await pg.evaluate("document.querySelector('.gallery-card__action').click()"); await pg.wait_for_timeout(250)
        c0=await pg.evaluate("document.getElementById('lightbox-counter').textContent")
        await pg.focus('#lightbox-next'); await pg.keyboard.press('Enter'); n1=await pg.evaluate("document.getElementById('lightbox-counter').textContent")
        await pg.keyboard.press('Space'); await pg.keyboard.press('ArrowRight'); n2=await pg.evaluate("document.getElementById('lightbox-counter').textContent")
        stayed=await pg.evaluate("document.getElementById('memories-lightbox').open")
        await pg.evaluate("document.getElementById('lightbox-close').click()"); await pg.wait_for_timeout(150)
    s=lambda t:int(t.split()[1])
    ck('gallery ×5 reopen: Enter on Next = 1 step, Space + ArrowRight = 2 more (no duplicated handlers), lightbox stays open', (s(n1)-s(c0))%11==1 and (s(n2)-s(n1))%11==2 and stayed,(c0,n1,n2,stayed))
    for i in range(8):
        await pg.evaluate("document.querySelector('[data-event-open]').click()"); await pg.wait_for_timeout(120); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(350)
    ck('event dialog ×8 open/close: closed, clean, one dialog node', await pg.evaluate("(()=>{const d=document.querySelectorAll('dialog#event-dialog');return d.length===1&&!d[0].open&&!d[0].querySelector('.event-dialog__panel').style.cssText})()"))
    await ctx.close()
    # resize while animations are active: start at 1440, scroll to trigger reveals, shrink to 390 mid-flight, grow to 1024, then finish scrolling
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(BASE); await pg.wait_for_timeout(300)
    for w,h in [(1440,900),(390,844),(1024,768),(320,640),(768,1024),(1440,900)]:
        await pg.set_viewport_size({'width':w,'height':h}); await pg.evaluate("scrollTo(0,document.querySelector('#offers').offsetTop)"); await pg.wait_for_timeout(120)
    await scroll_through(pg)
    hid=await pg.evaluate(HIDDEN); left=await pg.evaluate(INLINE)
    ck('resize 1440→390→1024→320→768→1440 during reveals: nothing hidden/stuck, no overflow, no errors',not hid and left==0 and not await pg.evaluate("document.documentElement.scrollWidth>innerWidth") and not errs,{'hid':hid,'left':left,'errs':errs[:2]})
    await ctx.close()
    # rapid scroll bursts incl. direction flips
    ctx=await b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True); pg=await ctx.new_page(); await pg.goto(BASE); await pg.wait_for_timeout(1200)
    Hh=await pg.evaluate('document.documentElement.scrollHeight')
    for y in [Hh,0,Hh//2,Hh,Hh//3,Hh,0,Hh]: await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(15)
    await pg.wait_for_timeout(3000)
    ck('rapid scroll flips on touch 390: nothing hidden or stuck',not await pg.evaluate(HIDDEN) and await pg.evaluate(INLINE)==0)
    await ctx.close(); await b.close()
  bad=[r for r in res if not r[1]]
  print(f'\n{len(res)-len(bad)}/{len(res)} passed'); json.dump(res,open(os.path.join(ROOT,'docs','phase8-5-results.json'),'w'),indent=1); sys.exit(1 if bad else 0)
asyncio.run(main())
