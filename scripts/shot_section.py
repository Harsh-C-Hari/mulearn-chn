#!/usr/bin/env python3
"""Screenshot one section (by CSS selector) at the five audit widths with a local server. Usage: shot_section.py <selector> <prefix> [pad_px]
Forces lazy images + waits for entrance animations; reports horizontal overflow."""
import sys,os,json,subprocess,time
from playwright.sync_api import sync_playwright
sel,prefix=sys.argv[1],sys.argv[2]; pad=int(sys.argv[3]) if len(sys.argv)>3 else 0
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
srv=subprocess.Popen([sys.executable,'-m','http.server','8766'],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
res={}
try:
  with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1024,1440):
      pg=b.new_page(viewport={'width':w,'height':900}); errs=[]
      pg.on('console',lambda m,e=errs:e.append(m.text) if m.type=='error' else None)
      pg.goto('http://localhost:8766/index.html'); pg.wait_for_timeout(600)
      pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
      pg.evaluate("document.querySelector(%r).scrollIntoView()"%sel); pg.wait_for_timeout(2200)
      pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(200)
      m=pg.evaluate('({sw:document.documentElement.scrollWidth,iw:innerWidth})')
      pg.add_style_tag(content='.site-header{position:static!important}.skip-link{display:none!important}')
      pg.wait_for_timeout(100)
      if pad: pg.screenshot(path=f'docs/screenshots/{prefix}-{w}.png',full_page=True)
      else:
        bb=pg.evaluate("(s)=>{const r=document.querySelector(s).getBoundingClientRect();return {x:0,y:r.top+scrollY,w:innerWidth,h:r.height}}",sel)
        pg.screenshot(path=f'docs/screenshots/{prefix}-{w}.png',full_page=True,clip={'x':0,'y':bb['y'],'width':bb['w'],'height':bb['h']})
      res[w]={'overflow':m['sw']>m['iw'],'sw':m['sw'],'console':errs}; pg.close()
    b.close()
finally: srv.terminate()
print(json.dumps(res))
