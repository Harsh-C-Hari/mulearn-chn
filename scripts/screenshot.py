#!/usr/bin/env python3
"""Screenshot a local HTML file at 320/390/768/1024/1440 and report horizontal overflow.
Usage: python3 scripts/screenshot.py <file.html> [outdir] [prefix]"""
import sys, os, json, asyncio
from playwright.async_api import async_playwright
WIDTHS=[320,390,768,1024,1440]
async def main(path,outdir,prefix):
    os.makedirs(outdir,exist_ok=True); res={}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w in WIDTHS:
            pg=await b.new_page(viewport={'width':w,'height':900})
            errs=[];reqs=[]
            pg.on('console',lambda m,e=errs: e.append(m.text) if m.type=='error' else None)
            pg.on('request',lambda r,q=reqs: q.append(r.url))
            await pg.goto('file://'+os.path.abspath(path)); await pg.wait_for_timeout(500)
            await pg.evaluate('document.fonts.ready')
            await pg.evaluate('''async()=>{document.querySelectorAll('img[loading=lazy]').forEach(i=>{i.loading='eager'});await Promise.race([Promise.all([...document.images].map(i=>i.decode?i.decode().catch(()=>0):0)),new Promise(r=>setTimeout(r,4000))])}''')
            await pg.wait_for_timeout(300)
            m=await pg.evaluate('({sw:document.documentElement.scrollWidth,iw:innerWidth,h:document.documentElement.scrollHeight})')
            wide=await pg.evaluate('''()=>{const iw=innerWidth,out=[];document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&r.right>iw+1&&!e.closest('[data-allow-overflow]'))out.push((e.className&&e.className.baseVal===undefined?e.className:e.tagName)+' '+Math.round(r.right))});return out.slice(0,8)}''')
            await pg.screenshot(path=f'{outdir}/{prefix}-{w}.png',full_page=True)
            ext=[r for r in reqs if not r.startswith('file://') and not r.startswith('data:')]
            res[w]={'scrollWidth':m['sw'],'innerWidth':m['iw'],'overflow':m['sw']>m['iw'],'pageHeight':m['h'],'consoleErrors':errs,'externalRequests':ext,'elementsBeyondViewport':wide}
            await pg.close()
        await b.close()
    print(json.dumps(res,indent=1)); return res
if __name__=='__main__':
    asyncio.run(main(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else 'docs/screenshots',sys.argv[3] if len(sys.argv)>3 else 'page'))
