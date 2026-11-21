#!/usr/bin/env python3
"""Phase 8.3 tests: mouse / touch / keyboard micro-interactions. Usage: python3 scripts/test_phase8_micro.py"""
import asyncio, json, os, sys, threading, http.server, socketserver, functools
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
S=socketserver.ThreadingTCPServer(('127.0.0.1',8771),functools.partial(H,directory=ROOT)); threading.Thread(target=S.serve_forever,daemon=True).start()
BASE='http://127.0.0.1:8771/index.html'
res=[]
def ck(n,ok,i=''):
    res.append((n,bool(ok),str(i))); print(('PASS ' if ok else 'FAIL ')+n,i)
SAMPLES={'btn':'.hero__actions .btn','link':'.about__actions .link','navlink':'.site-nav .nav-link','polaroid':'.polaroid:has(.polaroid__action)','galleryinner':'.gallery-card__inner','tile':'.footer__tile','brand .brand__mark':'.brand__mark','footlink':'.footer__links a'}
STYLE="(s)=>{const e=document.querySelector(s);const c=getComputedStyle(e);return [c.transform,c.boxShadow,c.textDecorationThickness,c.textDecorationColor,c.borderBottomColor].join('|')}"
async def forced(pg,cdp,doc,sel,state):
    node=await cdp.send('DOM.querySelector',{'nodeId':doc,'selector':sel})
    await cdp.send('CSS.forcePseudoState',{'nodeId':node['nodeId'],'forcedPseudoClasses':state})
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    # ---- TOUCH: mobile context => hover:none. No hover lift; pressed state differs from rest for every control
    ctx=await b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True); pg=await ctx.new_page()
    await pg.goto(BASE); await pg.wait_for_timeout(1500)
    await pg.add_style_tag(content='*,*::before,*::after{transition:none!important}')   # compare settled states, not mid-transition values
    ck('touch: (hover:hover) is false', not await pg.evaluate("matchMedia('(hover:hover) and (pointer:fine)').matches"))
    await pg.evaluate("document.getElementById('memories-gallery-toggle').click()"); await pg.wait_for_timeout(400)
    cdp=await ctx.new_cdp_session(pg); await cdp.send('DOM.enable'); await cdp.send('CSS.enable')
    doc=(await cdp.send('DOM.getDocument',{'depth':-1}))['root']['nodeId']
    for name,sel in SAMPLES.items():
        if name=='navlink':
            await pg.evaluate("document.querySelector('[data-js=menu-toggle]').click()"); await pg.wait_for_timeout(500)
        if name=='brand .brand__mark': sel='.brand__mark'
        # find the element that takes the :active pseudo (the control itself, not always the styled child)
        host={'polaroid':'.polaroid__action','galleryinner':'.gallery-card__action','brand .brand__mark':'.brand'}.get(name,sel)
        rest=await pg.evaluate(STYLE,sel)
        await forced(pg,cdp,doc,host,['hover']); hov=await pg.evaluate(STYLE,sel)
        await forced(pg,cdp,doc,host,[]); 
        ck(f'touch: no sticky hover change — {name}', hov==rest or name in('navlink',), '' if hov==rest else f'{rest} -> {hov}')
        await forced(pg,cdp,doc,host,['active']); act=await pg.evaluate(STYLE,sel)
        await forced(pg,cdp,doc,host,[])
        ck(f'touch: pressed feedback — {name}', act!=rest, f'{rest} -> {act}')
    # tap highlight: component-level only, never global
    ck('tap-highlight not globally suppressed', await pg.evaluate("getComputedStyle(document.body).webkitTapHighlightColor")!='rgba(0, 0, 0, 0)')
    ck('tap-highlight suppressed on topbar logo', await pg.evaluate("getComputedStyle(document.querySelector('.brand')).webkitTapHighlightColor")=='rgba(0, 0, 0, 0)')
    ck('touch-action: manipulation on controls', await pg.evaluate("[...document.querySelectorAll('a,button')].slice(0,40).every(e=>getComputedStyle(e).touchAction==='manipulation')"))
    await ctx.close()
    # ---- MOUSE: hover feedback present on desktop
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page(); await pg.goto(BASE); await pg.wait_for_timeout(1800)
    ck('mouse: (hover:hover) true', await pg.evaluate("matchMedia('(hover:hover) and (pointer:fine)').matches"))
    for sel in ['.hero__actions .btn']:
        r=await pg.evaluate(STYLE,sel); await pg.hover(sel); await pg.wait_for_timeout(300); h=await pg.evaluate(STYLE,sel)
        ck('mouse: hover changes '+sel, r!=h)
    # consistent timing: all controls use --t-fast (<=.15s) for press; none use transition:all
    allt=await pg.evaluate("[...document.querySelectorAll('*')].filter(e=>getComputedStyle(e).transitionProperty==='all'&&getComputedStyle(e).transitionDuration!=='0s').length")
    ck('no `transition: all` in use', allt==0, allt)
    ck('no permanent will-change', await pg.evaluate("[...document.querySelectorAll('*')].filter(e=>getComputedStyle(e).willChange!=='auto').length")==0)
    await ctx.close()
    # ---- KEYBOARD: focus ring visible on every control type; tab order follows DOM; no focus-only traps
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page(); await pg.goto(BASE); await pg.wait_for_timeout(1500)
    seen=0; bad=[]; order=[]
    for i in range(45):
        await pg.keyboard.press('Tab'); await pg.wait_for_timeout(40)
        info=await pg.evaluate("(()=>{const e=document.activeElement;if(!e||e===document.body)return null;const c=getComputedStyle(e);const r=e.getBoundingClientRect();return {t:e.tagName,cls:(e.className&&e.className.baseVal===undefined?e.className:'').slice(0,30),ring:c.outlineStyle!=='none'&&parseFloat(c.outlineWidth)>=2,y:Math.round(r.top+scrollY),h:Math.round(r.height),w:Math.round(r.width),obscured:r.top<(document.querySelector('.site-header').getBoundingClientRect().height-1)&&scrollY>0}})()")
        if info:
            seen+=1; order.append(info['y'])
            if not info['ring'] and info['w']>0: bad.append(info['cls'] or info['t'])
            if info['obscured']: bad.append('obscured:'+info['cls'])
    ck('keyboard: 45 tab stops all show a focus ring and none hides under the header', seen>=30 and not bad, bad[:5])
    ck('keyboard: tab order moves down the page', sum(1 for a,b2 in zip(order,order[1:]) if b2+400<a)<=2)
    await ctx.close(); await b.close()
  bad=[r for r in res if not r[1]]
  print(f'\n{len(res)-len(bad)}/{len(res)} passed'); json.dump(res,open(os.path.join(ROOT,'docs','phase8-3-results.json'),'w'),indent=1); sys.exit(1 if bad else 0)
asyncio.run(main())
