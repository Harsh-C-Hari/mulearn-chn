#!/usr/bin/env python3
"""Phase 5 tests (grows per subphase). Usage: python3 scripts/test_phase5.py [root_dir] [--sub N]
5.1: data integrity + content-accuracy guards, section structure/anchor/order, no overflow, no console errors, no external requests."""
import sys,os,json,subprocess,time,re
from playwright.sync_api import sync_playwright
args=[a for a in sys.argv[1:] if not a.startswith('--')]
root=os.path.abspath(args[0]) if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
srv=subprocess.Popen([sys.executable,'-m','http.server','8772'],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
URL='http://localhost:8772/index.html'; out={}; fails=[]
def chk(name,ok,info=''):
    out[name]={'pass':bool(ok),'info':info}
    if not ok: fails.append(name)
    print(('PASS ' if ok else 'FAIL ')+name+(' — '+str(info) if info and not ok else ''))
try:
  # ---- data (node) ----
  js=r'''global.window={};require("./data/events.js");console.log(JSON.stringify(window.MULEARN.events))'''
  ev=json.loads(subprocess.check_output(['node','-e',js],cwd=root).decode())
  by={e['slug']:e for e in ev}
  chk('seven canonical events',[e['title'] for e in sorted(ev,key=lambda e:e['order'])]==['ODYSSEY','Buildathon','Build with AI','Tech Forge','Type Race','Useless Projects 3.0','Web Slingers'])
  chk('grouping 3 featured + 4 compact',[e['slug'] for e in ev if e['group']=='featured']==['odyssey','buildathon','bwai'] and len([e for e in ev if e['group']=='compact'])==4)
  blob=json.dumps(ev,ensure_ascii=False)
  chk('no null/empty values in displayable fields',not re.search(r'"(value|name|label|role)":\s*(null|"")',blob) and all(isinstance(f.get('value'),str) and f['value'] for e in ev for f in (e.get('facts') or [])))
  chk('no "upcoming"/"register now" language',not re.search(r'upcoming|register now|coming soon|join us on',blob,re.I))
  chk('years only where printed (Buildathon/Useless/WebSlingers have none)',all(not re.search(r'20\d\d',json.dumps([e.get('dateLabel'),e.get('facts')],ensure_ascii=False)) for e in (by['buildathon'],by['useless'],by['webslingers'])))
  chk('Tech Forge carries no invented details',by['techforge']['facts']==[] and not by['techforge'].get('dateLabel') and 'venue' not in json.dumps(by['techforge']['facts']).lower() and 'lists' not in by['techforge'])
  chk('ODYSSEY facts match poster',{f['label']:f['value'] for f in by['odyssey']['facts']}=={'Date':'20–21 September 2026','Duration':'32 hours','Venue':'College of Engineering, Chengannur','Prize pool':'₹15,000','Registration fee':'₹150','Registration':'MakeMyPass'} and '24' not in json.dumps(by['odyssey']['facts']))
  chk('Buildathon prize keeps asterisk, no year',{f['label']:f['value'] for f in by['buildathon']['facts']}['Prize pool']=='₹7K*')
  bw=json.dumps(by['bwai'],ensure_ascii=False)
  chk('Build with AI: two separate parts, disputed location omitted',len(by['bwai']['parts'])==2 and 'Alappuzha' not in json.dumps({k:v for k,v in by['bwai'].items() if k!='open'}) and 'MCA CC2' in bw and 'Maker’s Space & SDPK' in bw)
  tr={f['label']:f['value'] for f in by['typerace']['facts']}
  chk('Type Race eligibility exact',tr['Free entry']=='µLearners with 7K+ Karma points and IEEE CS members (5 seats)' and tr['Registration fee']=='₹20')
  chk('Web Slingers venue/time per register',{f['label']:f['value'] for f in by['webslingers']['facts']}=={'Date':'27 October','Time':'4:00–5:15 PM','Venue':'SDPK Room 204'})
  chk('Useless Projects: no winners, no venue',not any(l['label']=='Winners' for l in by['useless'].get('lists',[])) and not any(f['label']=='Venue' for f in by['useless']['facts']))
  missing=[p for e in ev for p in [e['image']['card']['src'],e['image']['poster']['src']]+[x['src'] for x in e.get('photos',[])]+[s.split()[0] for s in e['image']['card']['srcset'].split(',')] if not os.path.exists(os.path.join(root,p.strip()))]
  chk('all event image references exist',not missing,missing)
  chk('every informative image has alt text',all(e['image'].get('alt') and all(p.get('alt') for p in e.get('photos',[])) for e in ev))
  chk('no source assets referenced',not re.search(r'sources/',blob))
  chk('index.html event markup is generated from data',subprocess.call(['node','scripts/build_events.js','--check'],cwd=root,stdout=subprocess.DEVNULL)==0)
  with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1024,1440):
      pg=b.new_page(viewport={'width':w,'height':900}); errs=[]; ext=[]
      pg.on('console',lambda m,errs=errs: errs.append(m.text) if m.type=='error' else None)
      pg.on('pageerror',lambda e,errs=errs: errs.append(str(e)))
      pg.on('request',lambda r,ext=ext: ext.append(r.url) if not r.url.startswith(('http://localhost','data:')) else None)
      pg.goto(URL); pg.wait_for_timeout(1200)
      if w==1440:
        order=pg.evaluate("[...document.querySelectorAll('main > section, main > .anchor-stubs span')].map(e=>e.id||e.className)")
        chk('section order hero→about→offers→events→team→memories→join',[o for o in order if o in('hero','about','offers','events','team','memories','join')]==['hero','about','offers','events','team','memories','join'],order)
        chk('#events is the real section (not a stub)',pg.evaluate("document.getElementById('events').tagName")=='SECTION')
        chk('single h2 with proper labelling',pg.evaluate("(()=>{const s=document.getElementById('events');const h=[...s.querySelectorAll('h2')];return h.length==1&&s.getAttribute('aria-labelledby')==h[0].id})()"))
        chk('seven h3 event titles, 3 featured + 4 compact',pg.evaluate("[document.querySelectorAll('.events__featured > li h3').length,document.querySelectorAll('.events__compact > li h3').length]")==[3,4])
        chk('nav + hero CTA resolve to #events below the sticky header',pg.evaluate("""()=>{document.documentElement.style.scrollBehavior='auto';document.querySelector('.site-nav a[href="#events"]').click();return new Promise(r=>setTimeout(()=>{const t=document.getElementById('events').getBoundingClientRect().top;const h=document.querySelector('.site-header').getBoundingClientRect().height;r(t>=h-4&&t<h+80)},400))}"""))
      ov=pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
      chk(f'{w}px: no horizontal overflow',ov<=0,ov)
      clip=pg.evaluate("[...document.querySelectorAll('.event__title')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent)")
      chk(f'{w}px: no clipped event titles',not clip,clip)
      chk(f'{w}px: no console errors',not errs,errs); chk(f'{w}px: no external requests',not ext,ext)
      pg.close()
    b.close()
finally:
  srv.terminate()
json.dump(out,open(os.path.join(root,'docs','phase5-results.json'),'w'),indent=1,ensure_ascii=False)
print(f"\n{len(out)-len(fails)}/{len(out)} passed"); sys.exit(1 if fails else 0)
