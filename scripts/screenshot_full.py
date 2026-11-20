#!/usr/bin/env python3
"""Full-page screenshots in the FINAL animated state: scroll through the page so scroll reveals fire, wait, return to top.
Usage: python3 scripts/screenshot_full.py [outdir] [prefix]"""
import sys, os, asyncio
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'docs/screenshots'); PRE=sys.argv[2] if len(sys.argv)>2 else 'full'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w in (320,390,768,1024,1440):
            pg=await b.new_page(viewport={'width':w,'height':900})
            await pg.goto('file://'+os.path.join(ROOT,'index.html')); await pg.wait_for_timeout(2800)
            h=await pg.evaluate('document.documentElement.scrollHeight')
            for y in range(0,h,300): await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(120)
            await pg.wait_for_timeout(2500); await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f'{OUT}/{PRE}-{w}.png',full_page=True); await pg.close()
        await b.close()
asyncio.run(main())
