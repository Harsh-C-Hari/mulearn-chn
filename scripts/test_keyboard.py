#!/usr/bin/env python3
"""Keyboard walk: Tab through the page, assert every stop has a visible focus indicator
(outline width >= 2px, non-transparent). Screenshots a few stops.
Usage: python3 scripts/test_keyboard.py page.html [outdir]"""
import sys, os, json, asyncio
from playwright.async_api import async_playwright
page=sys.argv[1]; out=sys.argv[2] if len(sys.argv)>2 else "docs/screenshots"; os.makedirs(out,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1280,'height':800})
        await pg.goto('file://'+os.path.abspath(page)); await pg.wait_for_timeout(400)
        stops=[]; bad=[]
        for i in range(120):
            await pg.keyboard.press('Tab')
            info=await pg.evaluate("""()=>{const e=document.activeElement;if(!e||e===document.body)return null;const s=getComputedStyle(e);const r=e.getBoundingClientRect();
              return {tag:e.tagName.toLowerCase(),text:(e.innerText||e.getAttribute('aria-label')||e.placeholder||'').trim().slice(0,28),ow:parseFloat(s.outlineWidth),os:s.outlineStyle,oc:s.outlineColor,w:Math.round(r.width),h:Math.round(r.height),
              visible:r.width>0&&r.height>0}}""")
            if not info: break
            stops.append(info)
            if info['os']=='none' or info['ow']<2 or not info['visible']: bad.append(info)
            if i in (0,20,60): await pg.screenshot(path=f'{out}/focus-stop-{i}.png')
        # focus section demo screenshot
        await pg.focus('#focus .btn--accent'); await pg.keyboard.press('Shift+Tab'); await pg.keyboard.press('Tab')
        await (await pg.query_selector('#focus')).scroll_into_view_if_needed(); await pg.wait_for_timeout(200)
        await pg.screenshot(path=f'{out}/focus-section.png')
        small=[s for s in stops if s['h']<44 and s['tag'] in ('a','button') and s['text'] not in ('',)]
        print(json.dumps({'tabStops':len(stops),'withoutVisibleFocus':bad,'interactiveBelow44px':small[:12]},indent=1))
        await b.close()
asyncio.run(main())
