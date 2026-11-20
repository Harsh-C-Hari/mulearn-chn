#!/usr/bin/env python3
"""Phase 3.1 header test: screenshots at 5 widths, menu open/close/Esc/focus return, overflow, sticky, nav-fit.
Usage: python3 scripts/test_header.py [outdir]"""
import sys,os,json,asyncio
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'docs/screenshots')
os.makedirs(OUT,exist_ok=True)
URL='file://'+os.path.join(ROOT,'index.html')
W=[320,390,768,1024,1180,1440]
async def main():
    res={}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w in W:
            pg=await b.new_page(viewport={'width':w,'height':800}); errs=[]
            pg.on('console',lambda m,e=errs:e.append(m.text) if m.type=='error' else None)
            pg.on('pageerror',lambda e,x=errs:x.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(500); await pg.evaluate('document.fonts.ready')
            r={}
            r['overflow']=await pg.evaluate('document.documentElement.scrollWidth>innerWidth')
            r['headerH']=await pg.evaluate('document.querySelector(".site-header").getBoundingClientRect().height')
            desktop=w>=1180
            tog=pg.locator('[data-js=menu-toggle]')
            r['toggleVisible']=await tog.is_visible()
            r['navVisible']=await pg.locator('#site-nav').is_visible()
            if desktop:
                rows=await pg.evaluate('''()=>{const l=[...document.querySelectorAll('.site-nav .nav-link')];return new Set(l.map(e=>Math.round(e.getBoundingClientRect().top))).size}''')
                r['navSingleRow']=rows==1
                r['ctaVisible']=await pg.locator('.site-nav__cta a').is_visible()
            await pg.screenshot(path=f'{OUT}/header-{w}.png',clip={'x':0,'y':0,'width':w,'height':120 if desktop else 120})
            if not desktop:
                await tog.focus(); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(150)
                r['expandedAfterOpen']=await tog.get_attribute('aria-expanded')
                r['panelVisible']=await pg.locator('#site-nav').is_visible()
                await pg.screenshot(path=f'{OUT}/header-{w}-menu-open.png',clip={'x':0,'y':0,'width':w,'height':640})
                r['overflowOpen']=await pg.evaluate('document.documentElement.scrollWidth>innerWidth')
                await pg.keyboard.press('Escape'); await pg.wait_for_timeout(100)
                r['expandedAfterEsc']=await tog.get_attribute('aria-expanded')
                r['focusReturned']=await pg.evaluate('document.activeElement===document.querySelector("[data-js=menu-toggle]")')
                await tog.click(); await pg.locator('#site-nav a[href="#about"]').click(); await pg.wait_for_timeout(200)
                r['closedAfterLink']=await tog.get_attribute('aria-expanded')
                await tog.click(); await pg.mouse.click(5,790); await pg.wait_for_timeout(100)
                r['closedAfterOutside']=await tog.get_attribute('aria-expanded')
            # sticky
            await pg.evaluate('window.scrollTo(0,600)'); await pg.wait_for_timeout(300)
            r['stickyTop']=await pg.evaluate('Math.round(document.querySelector(".site-header").getBoundingClientRect().top)')
            r['hrefs']=await pg.evaluate('[...document.querySelectorAll("[data-link]")].map(a=>a.href)')
            r['console']=errs
            res[w]=r; await pg.close()
        b2=await b.new_context(java_script_enabled=False,viewport={'width':390,'height':800}); pg=await b2.new_page()
        await pg.goto(URL); await pg.wait_for_timeout(300)
        res['noJS']={'toggleVisible':await pg.locator('[data-js=menu-toggle]').is_visible(),'navVisible':await pg.locator('#site-nav').is_visible(),
                     'ctaVisible':await pg.locator('.site-nav__cta').is_visible(),'overflow':await pg.evaluate('document.documentElement.scrollWidth>innerWidth')}
        await pg.screenshot(path=f'{OUT}/header-390-nojs.png',clip={'x':0,'y':0,'width':390,'height':300})
        await b.close()
    print(json.dumps(res,indent=1)); json.dump(res,open(f'{OUT}/header-test.json','w'),indent=1)
asyncio.run(main())
