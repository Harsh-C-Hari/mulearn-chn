#!/usr/bin/env python3
"""Phase 3 audit: every element motion-home.js animates → does it carry a CSS transition on transform/opacity, and was it locked?"""
import sys, os, re, json, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def log_message(s, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), Q); threading.Thread(target=srv.serve_forever, daemon=True).start()
src = open(os.path.join(ROOT, 'js/motion-home.js')).read()
# every selector string literal that is animated: intro steps `sel:`, sticker selectors, rise(q(...)), hero q(...)
sels = set(re.findall(r'sel: "([^"]+)"', src)) | set(re.findall(r'"(\.[\w .>,*-]*(?:sticker|stk)[\w .>,*-]*svg)"', src))
sels |= set(re.findall(r'rise\(q\("([^"]+)"', src))
sels |= set(re.findall(r'q\("([^"]+)", hero\)', src))
sels |= {s.strip() for m in re.findall(r'var heroEls = q\("([^"]+)"', src) for s in m.split(',')}
sels = sorted(s for s in sels if s)
SEC = {'.about__card': '#about', '.offers__note': '#offers'}
OBS = """()=>{window.__L=new Set();const mo=new MutationObserver(r=>r.forEach(m=>{if(m.target.classList&&m.target.classList.contains('is-revealing'))window.__L.add(m.target)}));mo.observe(document,{subtree:true,attributes:true,attributeFilter:['class']})}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 800}); pg.set_default_timeout(15000)
    pg.add_init_script("(" + OBS + ")()")
    pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/index.html', wait_until='load'); pg.wait_for_timeout(1800)
    H = pg.evaluate("document.documentElement.scrollHeight")
    for y in range(0, H, 350): pg.evaluate("y=>window.scrollTo(0,y)", y); pg.wait_for_timeout(260)
    pg.evaluate("window.scrollTo(0,document.documentElement.scrollHeight)"); pg.wait_for_timeout(2500)
    rows = pg.evaluate("""sels=>sels.map(s=>{const els=[...document.querySelectorAll(s)];const tr=e=>{const c=getComputedStyle(e);return c.transitionProperty+'|'+c.transitionDuration};
      const withT=els.filter(e=>{const c=getComputedStyle(e),pr=c.transitionProperty.split(',').map(x=>x.trim()),du=c.transitionDuration.split(',').map(x=>parseFloat(x));return pr.some((x,i)=>(x==='all'||x==='transform'||x==='opacity')&&(du[i%du.length]>0))});
      const locked=els.filter(e=>window.__L.has(e));return {sel:s,n:els.length,withTransition:withT.length,locked:locked.length,unlockedWithTransition:withT.filter(e=>!window.__L.has(e)).length,leftover:els.filter(e=>e.classList.contains('is-revealing')).length,sample:withT[0]?tr(withT[0]):''}})""", sels)
    b.close()
bad = 0
print(f"{'selector':58} {'n':>3} {'css-trans':>9} {'locked':>6} {'unlocked+trans':>14}")
for r in rows:
    flag = '' if r['unlockedWithTransition'] == 0 and r['leftover'] == 0 else '  <-- PROBLEM'
    bad += bool(flag)
    print(f"{r['sel'][:58]:58} {r['n']:>3} {r['withTransition']:>9} {r['locked']:>6} {r['unlockedWithTransition']:>14}{flag}")
json.dump(rows, open(os.path.join(ROOT, 'docs', 'reveal-lock-audit.json'), 'w'), indent=1)
print('AUDIT', 'PASS (no animated element with a CSS transform/opacity transition escaped the lock)' if not bad else 'FAIL'); sys.exit(1 if bad else 0)
