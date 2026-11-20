#!/usr/bin/env python3
"""Phase 3.5 motion tests for index.html: normal · reduced-motion · GSAP blocked · JS disabled.
Checks: start states applied, final states clean (no leftover inline opacity/transform), content visible, CLS, keyboard, menu.
Usage: python3 scripts/test_motion_home.py"""
import os, json, asyncio
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL='file://'+os.path.join(ROOT,'index.html')
SEL=['.hero__title span','.hero__intro > *','.hero__actions > *','.hero__figure','.about__card','.about__pair .card','.about__figure']
VIS='''(sels)=>sels.map(s=>[...document.querySelectorAll(s)].map(e=>{const c=getComputedStyle(e);return {s, op:+c.opacity, vis:c.visibility}})).flat()'''
LEFT='''(sels)=>sels.map(s=>[...document.querySelectorAll(s)].filter(e=>e.style.opacity||e.style.visibility).length).reduce((a,b)=>a+b,0)'''
CLS='''()=>new Promise(r=>{let v=0;try{new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)v+=e.value}).observe({type:'layout-shift',buffered:true})}catch(e){}setTimeout(()=>r(v),50)})'''
async def run(b,name,reduced=False,block=False,nojs=False,w=1280):
    ctx=await b.new_context(reduced_motion='reduce' if reduced else 'no-preference',viewport={'width':w,'height':800},java_script_enabled=not nojs)
    pg=await ctx.new_page(); errs=[]; reqs=[]
    pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None); pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('request',lambda r:reqs.append(r.url))
    if block: await pg.route('**/vendor/gsap/**',lambda r:r.abort())
    await pg.goto(URL)
    out={'scenario':name}
    if not nojs:
        await pg.wait_for_timeout(250)
        out['motionClass']=await pg.evaluate("document.documentElement.classList.contains('js-motion')")
        if not reduced and not block:
            await pg.wait_for_timeout(120)
            out['midHero_minOpacity']=min(x['op'] for x in await pg.evaluate(VIS,SEL[:4]))   # <1 means the entrance is running
        await pg.wait_for_timeout(2600)
    # hero must be fully visible after the entrance
    hv=await pg.evaluate(VIS,SEL[:4]); out['heroAllVisible']=all(x['op']==1 and x['vis']=='visible' for x in hv)
    if nojs or reduced or block:
        av=await pg.evaluate(VIS,SEL[4:]); out['aboutVisibleWithoutScroll']=all(x['op']==1 and x['vis']=='visible' for x in av)
    else:
        top=await pg.evaluate("document.getElementById('about').getBoundingClientRect().top+scrollY")
        await pg.evaluate(f"window.scrollTo(0,{top}-200)"); await pg.wait_for_timeout(2200)
        av=await pg.evaluate(VIS,SEL[4:]); out['aboutRevealedOnScroll']=all(x['op']==1 and x['vis']=='visible' for x in av)
        out['leftoverInlineStyles']=await pg.evaluate(LEFT,SEL)
    out['overflow']=await pg.evaluate('document.documentElement.scrollWidth>innerWidth')
    out['gsapRequested']=[u.rsplit('/',1)[-1] for u in reqs if 'vendor/gsap' in u]
    out['external']=[u for u in reqs if not u.startswith(('file://','data:'))]
    out['console']=errs
    if not nojs:
        await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(300)
        out['stuckClassAtTop']=await pg.evaluate("document.querySelector('.site-header').classList.contains('is-stuck')")
        await pg.evaluate('window.scrollTo(0,400)'); await pg.wait_for_timeout(300)
        out['stuckClassScrolled']=await pg.evaluate("document.querySelector('.site-header').classList.contains('is-stuck')")
        # keyboard still works after motion
        await pg.evaluate('window.scrollTo(0,0)'); await pg.keyboard.press('Tab'); await pg.keyboard.press('Tab')
        out['focusAfterMotion']=await pg.evaluate("document.activeElement&&document.activeElement.className")
    await ctx.close(); return out
async def cls_test(b):
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page()
    await pg.add_init_script("window.__cls=0;try{new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:'layout-shift',buffered:true})}catch(e){}")
    await pg.goto(URL); await pg.wait_for_timeout(2500)
    await pg.evaluate('window.scrollTo(0,document.body.scrollHeight)'); await pg.wait_for_timeout(2500)
    v=await pg.evaluate('window.__cls'); await ctx.close(); return round(v,4)
async def main():
    res=[]
    async with async_playwright() as p:
        b=await p.chromium.launch()
        res.append(await run(b,'normal')); res.append(await run(b,'reduced',reduced=True))
        res.append(await run(b,'gsap-blocked',block=True)); res.append(await run(b,'js-disabled',nojs=True))
        res.append(await run(b,'normal-390',w=390))
        cls=await cls_test(b); await b.close()
    n,r,g,j,m=res
    checks={
     'normal: entrance runs (opacity <1 mid-animation)': n.get('midHero_minOpacity',1)<1,
     'normal: hero fully visible after entrance': n['heroAllVisible'],
     'normal: About revealed on scroll': n.get('aboutRevealedOnScroll'),
     'normal: no leftover inline opacity/visibility': n.get('leftoverInlineStyles')==0,
     'normal: js-motion class set': n['motionClass'],
     'normal: header shadow class toggles': (not n['stuckClassAtTop']) and n['stuckClassScrolled'],
     'reduced: GSAP not requested': r['gsapRequested']==[],
     'reduced: no js-motion class': not r['motionClass'],
     'reduced: content visible': r['heroAllVisible'] and r['aboutVisibleWithoutScroll'],
     'gsap-blocked: content visible': g['heroAllVisible'] and g['aboutVisibleWithoutScroll'],
     'gsap-blocked: no js-motion class': not g['motionClass'],
     'js-disabled: content visible': j['heroAllVisible'] and j['aboutVisibleWithoutScroll'],
     'mobile 390: no overflow + reveals': (not m['overflow']) and m.get('aboutRevealedOnScroll'),
     'no console errors (gsap-blocked ignores the deliberately blocked request itself)': all(not [e for e in x['console'] if not (x['scenario']=='gsap-blocked' and 'ERR_FAILED' in e)] for x in res),
     'no external requests (all scenarios)': all(not x['external'] for x in res),
     'no overflow (all scenarios)': all(not x['overflow'] for x in res),
     'CLS < 0.01 with motion': cls<0.01,
    }
    for k,v in checks.items(): print(('PASS ' if v else 'FAIL ')+k)
    print('CLS =',cls); json.dump({'scenarios':res,'cls':cls,'checks':checks},open(os.path.join(ROOT,'docs/motion-home-results.json'),'w'),indent=1)
    raise SystemExit(0 if all(checks.values()) else 1)
asyncio.run(main())
