#!/usr/bin/env python3
"""Screenshot #events at 320/390/768/1024/1440 -> docs/screenshots/events-<sub>-<w>.png. Usage: python3 scripts/shot_events.py <tag>"""
import sys,os,subprocess,time
from playwright.sync_api import sync_playwright
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); tag=sys.argv[1] if len(sys.argv)>1 else 'x'
srv=subprocess.Popen([sys.executable,'-m','http.server','8773'],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1024,1440):
      pg=b.new_page(viewport={'width':w,'height':900}); pg.goto('http://localhost:8773/index.html'); pg.wait_for_timeout(800)
      pg.evaluate("document.getElementById('events').scrollIntoView()"); pg.wait_for_timeout(2200)
      pg.locator('#events').screenshot(path=os.path.join(root,'docs/screenshots',f'events-{tag}-{w}.png')); pg.close()
    b.close()
finally: srv.terminate()
