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
      clip=pg.evaluate("[...document.querySelectorAll('.event-card__title,.event-mini__title')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent)")
      chk(f'{w}px: no clipped event titles',not clip,clip)
      # ---- 5.2 featured cards ----
      pg.evaluate("document.querySelectorAll('#events img').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(1800)
      fc=pg.evaluate("""[...document.querySelectorAll('.events__featured > li')].map(li=>{const im=li.querySelector('.event-card__poster img'),b=li.querySelector('.event-card__btn'),r=b.getBoundingClientRect(),c=li.querySelector('.event-card').getBoundingClientRect();
        return {slug:li.dataset.event,h3:li.querySelector('h3').textContent,loaded:im.complete&&im.naturalWidth>0,alt:im.alt.length>20,nat:im.naturalWidth,shown:im.getBoundingClientRect().width,btnName:b.textContent.trim(),open:b.dataset.eventOpen,popup:b.getAttribute('aria-haspopup'),bw:r.width,bh:r.height,
        inView:c.left>=-1&&c.right<=innerWidth+1,posterHidden:getComputedStyle(li.querySelector('.event-card__poster')).display}})""")
      chk(f'{w}px: 3 featured cards in order',[f['slug'] for f in fc]==['odyssey','buildathon','bwai'] and [f['h3'] for f in fc]==['ODYSSEY','Buildathon','Build with AI'],fc)
      chk(f'{w}px: featured posters load, have alt, are not upscaled',all(f['loaded'] and f['alt'] and f['shown']<=f['nat']+1 for f in fc),fc)
      chk(f'{w}px: detail buttons named, wired to slug, >=44px tall',all(f['btnName'].startswith('View details for ') and f['open']==f['slug'] and f['popup']=='dialog' and f['bh']>=44 for f in fc),fc)
      chk(f'{w}px: featured cards inside viewport',all(f['inView'] for f in fc),fc)
      if w==1440:
        chk('featured cards use only verified facts (dates/tags match data)',pg.evaluate("[...document.querySelectorAll('.event-card__tags .tag')].map(t=>t.textContent)")==['20–21 September 2026','College of Engineering, Chengannur','17–18 July','5 PM – 9 AM','31 March and 6–7 April 2026','Session + hackathon'])
        chk('no year invented on Buildathon card',not re.search(r'20\d\d',pg.evaluate("document.querySelector('.event--buildathon').textContent")))
        chk('no Alappuzha / CEC conflict text on Build with AI card',not re.search(r'Alappuzha|CEC',pg.evaluate("document.querySelector('.event--bwai').textContent")))
        chk('keyboard: each featured button focusable, focus ring visible',pg.evaluate("""()=>[...document.querySelectorAll('.event-card__btn')].every(b=>{b.focus();return document.activeElement===b&&getComputedStyle(b).outlineStyle!=='none'&&parseFloat(getComputedStyle(b).outlineWidth)>=2})"""))
        chk('featured event stickers: 3 stickers inside article.event-card, 0 on li',pg.evaluate("document.querySelectorAll('.events__featured .event-card .event-card__stk').length")==3 and pg.evaluate("document.querySelectorAll('.events__featured > li > .event-card__stk').length")==0)
        chk('featured event stickers: 3 distinct shapes',len(set(pg.evaluate("[...document.querySelectorAll('.events__featured .event-card__stk use')].map(u=>u.getAttribute('href'))")))==3)
        chk('featured event stickers: aria-hidden and pointer-events none',pg.evaluate("""()=>[...document.querySelectorAll('.events__featured .event-card__stk')].every(s=>s.getAttribute('aria-hidden')==='true'&&getComputedStyle(s).pointerEvents==='none')"""))
        pg.mouse.move(0,0); pg.evaluate("document.querySelector('.events__featured .event-card').scrollIntoView({block:'center'})"); pg.wait_for_timeout(400)
        _ec=pg.locator('.events__featured .event-card').first; _eb0=_ec.bounding_box(); _es0=_ec.locator('.event-card__stk').bounding_box()
        pg.mouse.move(_eb0['x']+_eb0['width']/2,_eb0['y']+_eb0['height']/2); pg.wait_for_timeout(350)
        _eb1=_ec.bounding_box(); _es1=_ec.locator('.event-card__stk').bounding_box()
        _edc=(round(_eb1['x']-_eb0['x']),round(_eb1['y']-_eb0['y'])); _eds=(round(_es1['x']-_es0['x']),round(_es1['y']-_es0['y']))
        chk('hover: featured event card and sticker translate together (-3px, -3px)',_edc==_eds and _edc==(-3,-3),(_edc,_eds))
      # ---- 5.3 compact entries ----
      cc=pg.evaluate("""[...document.querySelectorAll('.events__compact > li')].map(li=>{const im=li.querySelector('.event-mini__thumb img'),b=li.querySelector('.event-mini__btn'),r=b.getBoundingClientRect(),c=li.querySelector('.event-mini').getBoundingClientRect();
        return {slug:li.dataset.event,h3:li.querySelector('h3').textContent,loaded:im.complete&&im.naturalWidth>0,alt:im.alt.length>20,nat:+(im.currentSrc.match(/-(\\d+)\\.webp/)||[0,im.naturalWidth])[1],shown:im.getBoundingClientRect().width,btnName:b.textContent.trim(),open:b.dataset.eventOpen,popup:b.getAttribute('aria-haspopup'),bh:r.height,
        inView:c.left>=-1&&c.right<=innerWidth+1,date:(li.querySelector('.event-mini__date')||{}).textContent||null,ar:im.getBoundingClientRect().width/im.getBoundingClientRect().height,nar:im.naturalWidth/im.naturalHeight}})""")
      chk(f'{w}px: 4 compact entries in order',[c['slug'] for c in cc]==['techforge','typerace','useless','webslingers'] and [c['h3'] for c in cc]==['Tech Forge','Type Race','Useless Projects 3.0','Web Slingers'],cc)
      chk(f'{w}px: compact thumbnails load, have alt, not upscaled, aspect preserved',all(c['loaded'] and c['alt'] and c['shown']<=c['nat']+1 and abs(c['ar']-c['nar'])<.03 for c in cc),cc)
      chk(f'{w}px: compact buttons named, wired, >=44px',all(c['btnName'].startswith('View details for ') and c['open']==c['slug'] and c['popup']=='dialog' and c['bh']>=44 for c in cc),cc)
      chk(f'{w}px: compact entries inside viewport',all(c['inView'] for c in cc),cc)
      chk(f'{w}px: all seven events visible (7 detail buttons)',pg.evaluate("document.querySelectorAll('.events [data-event-open]').length")==7)
      if w==1440:
        chk('compact dates only where verified (Tech Forge has none)',[c['date'] for c in cc]==[None,'26 March 2026','11–12 September','27 October'],cc)
        chk('Tech Forge entry shows only the title-card text',pg.evaluate("document.querySelector('.event--techforge .event-mini__body').innerText.replace(/\\s+/g,' ')")  in ('04 Tech Forge TECHFORGE 2.0 View details for Tech Forge','04 Tech Forge TECHFORGE 2.0 View details'),pg.evaluate("document.querySelector('.event--techforge .event-mini__body').innerText"))
        chk('compact visually subordinate (title smaller than featured)',pg.evaluate("parseFloat(getComputedStyle(document.querySelector('.event-mini__title')).fontSize)<parseFloat(getComputedStyle(document.querySelector('.event-card__title')).fontSize)"))
      chk(f'{w}px: no console errors',not errs,errs); chk(f'{w}px: no external requests',not ext,ext)
      pg.close()
    # ---------------- 5.4 dialogs ----------------
    def expected(e):
        t=[e['title']]+[f['value'] for f in e.get('facts',[])]
        for part in e.get('parts',[]): t+= [part['title']]+[f['value'] for f in part['facts']]
        for l in e.get('lists',[]): t+= [l['label']]+[i['name'] for i in l['items']]+[i['role'] for i in l['items'] if i.get('role')]
        t+=e.get('branding',[]); return t
    def dlg_state(pg): return pg.evaluate("""()=>{const d=document.getElementById('event-dialog');const r=d.getBoundingClientRect();const p=d.querySelector('.event-dialog__poster img');
      return {open:d.open,title:d.querySelector('#event-dialog-title').textContent,desc:d.querySelector('#event-dialog-desc').textContent,text:d.textContent.replace(/\\s+/g,' '),lab:d.getAttribute('aria-labelledby'),dby:d.getAttribute('aria-describedby'),
      modal:d.matches(':modal'),inView:r.top>=0&&r.left>=0&&r.bottom<=innerHeight+1&&r.right<=innerWidth+1,posterOk:!!p&&p.complete&&p.naturalWidth>0&&!!p.alt,
      photosOk:[...d.querySelectorAll('.event-dialog__photo img')].every(i=>i.complete&&i.naturalWidth>0&&i.alt.length>10),
      inside:d.contains(document.activeElement),active:document.activeElement.className,ov:document.documentElement.scrollWidth-document.documentElement.clientWidth,
      emptyHeads:[...d.querySelectorAll('h3')].filter(h=>!h.textContent.trim()).length,sections:[...d.querySelectorAll('h3')].map(h=>h.textContent)}}""")
    for w in (320,390,768,1024,1440):
      pg=b.new_page(viewport={'width':w,'height':800 if w>=768 else 700}); errs=[]
      pg.on('console',lambda m,errs=errs: errs.append(m.text) if m.type=='error' else None); pg.on('pageerror',lambda e,errs=errs: errs.append(str(e)))
      pg.goto(URL); pg.wait_for_timeout(1000)
      pg.evaluate("document.querySelectorAll('#events img').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(800)
      for slug,e in by.items():
        sel=f'[data-event-open="{slug}"]'
        pg.locator(sel).scroll_into_view_if_needed(); pg.locator(sel).focus(); pg.keyboard.press('Enter'); pg.wait_for_timeout(700)
        st=dlg_state(pg)
        ok=st['open'] and st['modal'] and st['title']==e['title'] and st['lab']=='event-dialog-title' and st['dby']=='event-dialog-desc' and all(x in st['text'] for x in expected(e))
        chk(f'{w}px {slug}: opens by keyboard with correct content',ok,{k:st[k] for k in ('open','modal','title')})
        chk(f'{w}px {slug}: focus moves into dialog, fits viewport, poster+photos load with alt, no overflow',st['inside'] and st['inView'] and st['posterOk'] and st['photosOk'] and st['ov']<=0 and st['emptyHeads']==0,st)
        if w==1440 or w==320:
          bad=re.search(r'undefined|null|NaN|upcoming|register now|Alappuzha|\bCEC\b',st['text'].replace('College of Engineering, Chengannur',''),re.I)
          chk(f'{w}px {slug}: no placeholder/conflict text',not bad and not (slug=='bwai' and re.search(r'\\bCEC\\b',st['text'])),bad.group(0) if bad else '')
          # panel scrolls internally rather than the page
          chk(f'{w}px {slug}: page scroll locked while open',pg.evaluate("getComputedStyle(document.body).overflow")=='hidden')
        # Tab trap: tab through more stops than there are controls; focus must never leave the dialog
        stay=True
        for _ in range(4):
          pg.keyboard.press('Tab'); stay&=pg.evaluate("document.getElementById('event-dialog').contains(document.activeElement)")
        pg.keyboard.press('Shift+Tab'); stay&=pg.evaluate("document.getElementById('event-dialog').contains(document.activeElement)")
        chk(f'{w}px {slug}: Tab/Shift+Tab keep focus inside',stay)
        if slug in('odyssey','techforge') and w in(320,1440): 
          pg.screenshot(path=os.path.join(root,'docs','screenshots',f'dialog-{slug}-{w}.png'))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
        back=pg.evaluate("({open:document.getElementById('event-dialog').open,same:document.activeElement.dataset.eventOpen})")
        chk(f'{w}px {slug}: Esc closes and focus returns to its trigger',(not back['open']) and back['same']==slug,back)
      if w in (390,1440):
        # close button + backdrop click return focus too
        sel='[data-event-open="typerace"]'; pg.locator(sel).focus(); pg.keyboard.press('Enter'); pg.wait_for_timeout(600)
        pg.locator('.event-dialog__close').click(); pg.wait_for_timeout(500)
        chk(f'{w}px close button closes + restores focus',pg.evaluate("!document.getElementById('event-dialog').open&&document.activeElement.dataset.eventOpen=='typerace'"))
        pg.locator(sel).click(); pg.wait_for_timeout(600)
        pg.mouse.click(3,3); pg.wait_for_timeout(500)
        chk(f'{w}px backdrop click closes + restores focus',pg.evaluate("!document.getElementById('event-dialog').open&&document.activeElement.dataset.eventOpen=='typerace'"))
        pg.locator(sel).click(); pg.wait_for_timeout(600)
        pg.mouse.click(w//2,pg.viewport_size['height']//2); pg.wait_for_timeout(300)
        chk(f'{w}px click inside dialog does not close it',pg.evaluate("document.getElementById('event-dialog').open"))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
      chk(f'{w}px dialogs: no console errors',not errs,errs)
      pg.close()
    # reduced motion: opens/closes instantly, no GSAP requested; GSAP blocked: still works
    for label,kw,block in (('reduced-motion',dict(reduced_motion='reduce'),None),('GSAP blocked',{},'**/vendor/gsap/**')):
      ctx=b.new_context(viewport={'width':1024,'height':800},**kw); pg=ctx.new_page(); reqs=[]
      pg.on('request',lambda r,reqs=reqs: reqs.append(r.url))
      if block: pg.route(block,lambda r: r.abort())
      pg.goto(URL); pg.wait_for_timeout(900)
      pg.locator('[data-event-open="odyssey"]').click(); pg.wait_for_timeout(120)
      st=pg.evaluate("({open:document.getElementById('event-dialog').open,op:getComputedStyle(document.querySelector('.event-dialog__panel')).opacity,anim:document.getAnimations().length})")
      chk(f'{label}: dialog opens immediately and fully visible',st['open'] and st['op']=='1',st)
      pg.keyboard.press('Escape'); pg.wait_for_timeout(60)
      chk(f'{label}: Esc closes promptly',pg.evaluate("!document.getElementById('event-dialog').open"))
      if label=='reduced-motion': chk('reduced-motion: GSAP not requested',not any('gsap' in u.lower() for u in reqs),reqs)
      ctx.close()
    # JS disabled: info still visible, dead buttons hidden
    ctx=b.new_context(java_script_enabled=False,viewport={'width':1024,'height':800}); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(600)
    r=pg.evaluate("({btns:[...document.querySelectorAll('[data-event-open]')].filter(x=>x.offsetParent!==null).length,titles:[...document.querySelectorAll('#events h3')].filter(x=>x.offsetParent!==null).length,dates:document.querySelectorAll('.event-card__tags .tag').length})")
    chk('JS disabled: all 7 event titles + facts visible, dead buttons hidden',r['btns']==0 and r['titles']==7 and r['dates']>=6,r)
    ctx.close()
    b.close()
finally:
  srv.terminate()
json.dump(out,open(os.path.join(root,'docs','phase5-results.json'),'w'),indent=1,ensure_ascii=False)
print(f"\n{len(out)-len(fails)}/{len(out)} passed"); sys.exit(1 if fails else 0)
