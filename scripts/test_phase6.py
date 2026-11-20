#!/usr/bin/env python3
"""Phase 6 tests (grows per subphase). Usage: python3 scripts/test_phase6.py [root_dir]
6.1 data integrity, 6.2 featured cards, 6.3 directory;, roster/role/photo guards, section structure + anchor + order, overflow, console, network."""
import sys,os,json,subprocess,time,re
from playwright.sync_api import sync_playwright
from PIL import Image
args=[a for a in sys.argv[1:] if not a.startswith('--')]
root=os.path.abspath(args[0]) if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT='8773'
srv=subprocess.Popen([sys.executable,'-m','http.server',PORT],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
URL=f'http://localhost:{PORT}/index.html'; out={}; fails=[]
def chk(name,ok,info=''):
    out[name]={'pass':bool(ok),'info':info}
    if not ok: fails.append(name)
    print(('PASS ' if ok else 'FAIL ')+name+(' — '+str(info) if info and not ok else ''))
ROSTER=[("Geetha S","Lead Enabler"),("Nithin Jayakumar","Campus Lead"),("Divyalakshmi","Campus Co-Lead"),("Govind J S","Creative Lead"),("Hanin C K","Operational Lead"),("Amanul Farhan","Technical Lead"),("Pavithra A","Media Lead"),("Albin Thomas","Content Lead"),("Melwin Shibu Mathew","Operational Team"),("Sara Shaji","Operational Team"),("Afsal S","Designer"),("Vismaya Gawri Krishnan","Designer"),("Karthika S","Content Team"),("Sreelakshmi M","Content Team"),("Parvathy Vinayan","Media Team"),("Brijith K Reji","Media Team"),("Adhi Narayan","IG Lead – AI"),("Al Ameen","IG Lead – UI/UX"),("Amal S","IG Lead – Cyber Security"),("Abhiram J","IG Lead – Web"),("Swathy J","IG Lead – Entrepreneurship")]
FEAT=[("Nithin Jayakumar","Campus Lead"),("Amanul Farhan","Technical Lead"),("Govind J S","Creative Lead"),("Hanin C K","Operational Lead")]
HELD={"Geetha S","Divyalakshmi","Swathy J"}   # titles in doubt: name only
def label(name,role):
    return None if name in HELD else role.replace('IG Lead','Interest Group Lead')
try:
  js=r'''global.window={};require("./data/team.js");console.log(JSON.stringify(window.MULEARN.team))'''
  T=json.loads(subprocess.check_output(['node','-e',js],cwd=root).decode())
  chk('21 members, canonical names and recorded roles in order',[(m['name'],m['role']) for m in sorted(T,key=lambda m:m['order'])]==ROSTER)
  chk('21 unique names / ids / orders',len({m['name'] for m in T})==21 and len({m['id'] for m in T})==21 and sorted(m['order'] for m in T)==list(range(1,22)))
  chk('no members from older summaries (Abhiram V, Aswin Sreekumar)',not re.search(r'Abhiram V\b|Aswin',json.dumps(T)))
  fe=sorted([m for m in T if m['featured']],key=lambda m:m['featuredOrder'])
  chk('four featured in spec order with spec roles',[(m['name'],m['role']) for m in fe]==FEAT)
  chk('featured tones set (yellow/indigo/mint rotation)',all(m['tone'] in('yellow','indigo','mint') for m in fe))
  chk('displayed role labels as designed (held titles = null, IG expanded)',all(m['roleLabel']==label(m['name'],m['role']) for m in T),[(m['name'],m['roleLabel']) for m in T if m['roleLabel']!=label(m['name'],m['role'])])
  chk('held titles: status unconfirmed + note recorded',all((m['roleStatus']=='unconfirmed')==(m['name'] in HELD) and (m['roleNote'] if m['name'] in HELD else True) for m in T))
  chk('Hanin: Operational Lead shown, wording note recorded',[m for m in T if m['name']=='Hanin C K'][0]['roleLabel']=='Operational Lead' and 'Operations' in [m for m in T if m['name']=='Hanin C K'][0]['roleNote'])
  bad=[];up=[]
  for m in T:
    ph=m['photo']
    for k in('src300','src600'):
      if not os.path.exists(os.path.join(root,ph[k])): bad.append(ph[k])
    if os.path.exists(os.path.join(root,ph['src600'])):
      w,h=Image.open(os.path.join(root,ph['src600'])).size
      if (w,h)!=(ph['w'],ph['h']): up.append((m['name'],w,h))
  chk('all 42 portrait files exist and recorded sizes are real (no upscaling)',not bad and not up,(bad,up))
  chk('no source assets referenced',not re.search(r'sources/',json.dumps(T)))
  chk('no invented fields (bio/social/links/email)',not re.search(r'"(bio|about|description|linkedin|instagram|github|email|url|href|social)"',json.dumps(T),re.I))
  chk('index.html team markup is generated from data',subprocess.call(['node','scripts/build_team.js','--check'],cwd=root,stdout=subprocess.DEVNULL)==0)
  with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1024,1440):
      pg=b.new_page(viewport={'width':w,'height':900}); errs=[];ext=[]
      pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
      pg.on('request',lambda r:ext.append(r.url) if not r.url.startswith(f'http://localhost:{PORT}') and not r.url.startswith('data:') else None)
      pg.goto(URL); pg.wait_for_timeout(700)
      if w==1440:
        chk('#team is a <section> labelled by its h2',pg.evaluate("(()=>{const s=document.getElementById('team');return s&&s.tagName==='SECTION'&&s.getAttribute('aria-labelledby')==='team-title'&&document.getElementById('team-title').tagName==='H2'})()"))
        chk('no empty #team stub span remains',pg.evaluate("document.querySelectorAll('.anchor-stubs #team').length===0 && document.querySelectorAll('#team').length===1"))
        chk('section order Offers > Events > Team > Memories stub > Join',pg.evaluate("(()=>{const o=[...document.querySelectorAll('main > section, main > .anchor-stubs')].map(e=>e.id||'stub');return o.join()})()") in ('hero,about,offers,events,team,stub,join', 'hero,about,offers,events,team,memories,join'))
        chk('nav Team link targets the real section',pg.evaluate("(()=>{const a=[...document.querySelectorAll('header a')].find(a=>a.getAttribute('href')==='#team');return !!a&&document.getElementById('team').tagName==='SECTION'})()"))
        chk('21 roster entries, 4 featured, names unique (no 25-member impression)',pg.evaluate("document.querySelectorAll('.roster > li').length")==21 and pg.evaluate("document.querySelectorAll('.team__featured > li').length")==4 and pg.evaluate("new Set([...document.querySelectorAll('.roster > li')].map(l=>l.dataset.member)).size")==21)
        chk('roster text = names in roster order',pg.evaluate("[...document.querySelectorAll('.roster .roster__name')].map(e=>e.textContent)")==[n for n,_ in ROSTER])
        chk('held titles are NOT in the page, other roles are',pg.evaluate("(()=>{const t=document.getElementById('team').innerText;return !/Lead Enabler|Co-Lead|Entrepreneurship/.test(t)&&/Technical Lead/.test(t)&&/Interest Group Lead – Web/.test(t)})()"))
        chk('no invented stats/bios in section',not re.search(r'\d+\+?\s*(years|projects|events|members strong)|award|experience',pg.evaluate("document.getElementById('team').innerText"),re.I))
        chk('featured team stickers: 4 stickers inside article.member-card, 0 on li',pg.evaluate("document.querySelectorAll('.team__featured .member-card .member-card__stk').length")==4 and pg.evaluate("document.querySelectorAll('.team__featured > li > .member-card__stk').length")==0)
        _stk_shapes=pg.evaluate("[...document.querySelectorAll('.team__featured .member-card__stk use')].map(u=>u.getAttribute('href'))")
        chk('featured team stickers: 4 distinct shapes',len(set(_stk_shapes))==4 and len(_stk_shapes)==4,_stk_shapes)
        chk('Hanin sticker is bolt (#s-bolt)',pg.evaluate("document.querySelector('[data-member=\"team-05-hanin\"] .member-card__stk use').getAttribute('href')")=='#s-bolt')
        chk('roster stickers: 21 stickers inside li.roster__item',pg.evaluate("document.querySelectorAll('.roster .roster__item .roster__stk').length")==21)
        chk('roster decorations: aria-hidden and pointer-events none',pg.evaluate("""()=>[...document.querySelectorAll('.roster__stk')].every(s=>s.getAttribute('aria-hidden')==='true'&&getComputedStyle(s).pointerEvents==='none')"""))
        _dist_check=pg.evaluate("""() => {
          const items = [...document.querySelectorAll('.roster__item')];
          const shapes = items.map(li => li.querySelector('.roster__stk use').getAttribute('href'));
          const colors = items.map(li => {
            const cls = li.querySelector('.roster__stk').className;
            const m = cls.match(/sticker--([a-z]+)/);
            return m ? m[1] : '';
          });
          const mats = ['yellow','mint','coral','indigo','yellow','mint','coral','indigo','yellow','mint','coral','indigo','yellow','mint','coral','indigo','yellow','mint','coral','indigo','yellow'];
          let errs = [];
          for (let i = 0; i < shapes.length; i++) {
            for (let j = i + 1; j <= Math.min(i + 6, shapes.length - 1); j++) {
              if (shapes[i] === shapes[j]) errs.push(`Shape repeat between ${i+1} and ${j+1}: ${shapes[i]}`);
            }
            for (let j = i + 1; j <= Math.min(i + 4, colors.length - 1); j++) {
              if (colors[i] === colors[j]) errs.push(`Color repeat between ${i+1} and ${j+1}: ${colors[i]}`);
            }
            if (colors[i] === mats[i]) errs.push(`Color equals mat at ${i+1}: ${colors[i]}`);
          }
          return errs;
        }""")
        chk('roster distance rules: shape >= 6, color >= 4, color != mat',len(_dist_check)==0,_dist_check)
        _mc=pg.locator('.team__featured .member-card').first; _mc.scroll_into_view_if_needed(); pg.wait_for_timeout(1600)
        pg.mouse.move(0,0); pg.wait_for_timeout(200)
        _r0=_mc.evaluate("c=>{const s=c.querySelector('.member-card__stk'),rc=c.getBoundingClientRect(),rs=s.getBoundingClientRect();return [rc.x,rc.y,rs.x,rs.y]}")
        _mc.hover(); pg.wait_for_timeout(350)
        _r1=_mc.evaluate("c=>{const s=c.querySelector('.member-card__stk'),rc=c.getBoundingClientRect(),rs=s.getBoundingClientRect();return [rc.x,rc.y,rs.x,rs.y]}")
        _mdc=(round(_r1[0]-_r0[0]),round(_r1[1]-_r0[1])); _mds=(round(_r1[2]-_r0[2]),round(_r1[3]-_r0[3]))
        chk('hover: featured member card and sticker translate together (-3px, -3px)',_mdc==_mds and _mdc==(-3,-3),(_mdc,_mds))
      _colls=pg.evaluate("""() => {
        const items = [...document.querySelectorAll('.roster__item')];
        const hits = [];
        function overlaps(r1, r2) {
          return !(r2.left >= r1.right || r2.right <= r1.left || r2.top >= r1.bottom || r2.bottom <= r1.top);
        }
        items.forEach((item, idx) => {
          const stk = item.querySelector('.roster__stk');
          if (!stk) return;
          const stkRect = stk.getBoundingClientRect();
          const texts = [...item.querySelectorAll('.roster__num, .roster__name, .roster__role, .roster__flag')];
          texts.forEach(t => {
            const range = document.createRange();
            range.selectNodeContents(t);
            for (const r of range.getClientRects()) {
              if (overlaps(stkRect, r)) hits.push({ idx: idx+1, text: t.textContent });
            }
          });
        });
        return hits;
      }""")
      chk(f'{w}: no sticker bounding box intersects any text rect',len(_colls)==0,_colls)
      chk(f'{w}: no horizontal overflow',pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth"),pg.evaluate("document.documentElement.scrollWidth"))
      chk(f'{w}: no console errors / external requests',not errs and not ext,(errs,ext))
      # ---- 6.3 directory ----
      ty=pg.evaluate("document.getElementById('team').getBoundingClientRect().top+scrollY"); th=pg.evaluate("document.getElementById('team').offsetHeight")
      for off in range(0,int(th)+900,450):
          pg.evaluate(f"window.scrollTo({{top:{ty}+{off}-200,behavior:'instant'}})"); pg.wait_for_timeout(150)
      pg.wait_for_timeout(900)
      rd=pg.evaluate("""()=>[...document.querySelectorAll('.roster > li')].map(l=>{const im=l.querySelector('img'),n=l.querySelector('.roster__name'),r=l.querySelector('.roster__role'),f=l.querySelector('.roster__flag'),b=l.getBoundingClientRect();
        return {name:n.textContent,role:r?r.textContent:null,flag:f?f.textContent:null,loaded:im.complete&&im.naturalWidth>0,alt:im.getAttribute('alt'),nat:im.naturalWidth,css:Math.round(im.getBoundingClientRect().width),clip:n.scrollWidth>n.clientWidth+1,inView:b.left>=-1&&b.right<=innerWidth+1,left:Math.round(b.left)}})""")
      chk(f'{w}: directory lists all 21 unique members with exact names and roles',[(i['name'],i['role']) for i in rd]==[(n,label(n,r)) for n,r in ROSTER],[(i['name'],i['role']) for i in rd][:3])
      chk(f'{w}: exactly the four featured are flagged "Featured above"',[i['name'] for i in rd if i['flag']]==[n for n,_ in FEAT] or sorted(i['name'] for i in rd if i['flag'])==sorted(n for n,_ in FEAT) and all(i['flag']=='Featured above' for i in rd if i['flag']))
      chk(f'{w}: featured cards and directory refer to the same 4 people (no 25-person count)',len(rd)==21 and {i['name'] for i in rd}>={n for n,_ in FEAT})
      chk(f'{w}: directory portraits loaded, decorative alt, not upscaled',all(i['loaded'] and i['alt']=='' and i['css']<=i['nat'] for i in rd),[(i['name'],i['nat'],i['css']) for i in rd if i['css']>i['nat']])
      chk(f'{w}: directory names not clipped, entries inside viewport',all(not i['clip'] and i['inView'] for i in rd))
      dc=len({i['left'] for i in rd})
      chk(f'{w}: directory columns {1 if w<700 else 2 if w<1024 else 3}',dc==(1 if w<700 else 2 if w<1024 else 3),dc)
      # ---- 6.2 featured cards ----
      pg.evaluate("document.getElementById('team').scrollIntoView({behavior:'instant'})"); pg.wait_for_timeout(1200)
      info=pg.evaluate("""()=>[...document.querySelectorAll('.team__featured .member-card')].map(c=>{const im=c.querySelector('img'),n=c.querySelector('.member-card__name'),r=c.querySelector('.member-card__role'),b=c.getBoundingClientRect();
        return {name:n.textContent,role:r?r.textContent:null,loaded:im.complete&&im.naturalWidth>0,alt:im.alt,cur:im.currentSrc.split('/').pop(),nat:im.naturalWidth,css:Math.round(im.getBoundingClientRect().width),nameClip:n.scrollWidth>n.clientWidth+1,inView:b.left>=-1&&b.right<=innerWidth+1,h:Math.round(b.height),tag:c.tagName,inter:c.querySelectorAll('a,button').length,hd:n.tagName}})""")
      chk(f'{w}: four featured cards, names and roles exact, in order',[(i['name'],i['role']) for i in info]==FEAT,[(i['name'],i['role']) for i in info])
      chk(f'{w}: featured portraits loaded with alt "Portrait of <name>"',all(i['loaded'] and i['alt']=='Portrait of '+i['name'] for i in info),info)
      chk(f'{w}: no portrait upscaled (CSS width <= file width)',all(i['css']<=i['nat'] for i in info),[(i['cur'],i['nat'],i['css']) for i in info])
      chk(f'{w}: names not clipped, cards inside viewport',all(not i['nameClip'] and i['inView'] for i in info))
      chk(f'{w}: names are h3 inside articles; cards carry no dead controls',all(i['hd']=='H3' and i['tag']=='ARTICLE' and i['inter']==0 for i in info))
      cols=pg.evaluate("new Set([...document.querySelectorAll('.team__featured > li')].map(l=>Math.round(l.getBoundingClientRect().left))).size")
      chk(f'{w}: layout columns {"1" if w<600 else "2" if w<1024 else "4"}',cols==(1 if w<600 else 2 if w<1024 else 4),cols)
      pg.close()
    pg=b.new_page(viewport={'width':1440,'height':900}); pg.goto(URL); pg.wait_for_timeout(700)
    pg.click('header a[href="#team"]')
    last=-1
    for _ in range(40):
        pg.wait_for_timeout(250); y=pg.evaluate('scrollY')
        if y==last: break
        last=y
    top=pg.evaluate("document.getElementById('team').getBoundingClientRect().top")
    chk('header Team link scrolls to the section, landing below the sticky header',60<=top<=130,top)
    # ---- 6.4 interaction & motion ----
    VIS="""()=>{const t=document.getElementById('team');const els=[...t.querySelectorAll('.team__head > *,.member-card,.roster-panel,.roster > li')];
      return {n:els.length,hidden:els.filter(e=>{const c=getComputedStyle(e);return c.visibility==='hidden'||c.display==='none'||parseFloat(c.opacity)<0.99}).length,
              roster:t.querySelectorAll('.roster > li').length,feat:t.querySelectorAll('.member-card').length,motion:document.documentElement.classList.contains('js-motion')}}"""
    def scroll_team(pg):
        ty=pg.evaluate("document.getElementById('team').getBoundingClientRect().top+scrollY"); th=pg.evaluate("document.getElementById('team').offsetHeight")
        for off in range(0,int(th)+900,400):
            pg.evaluate(f"window.scrollTo({{top:{ty}+{off}-200,behavior:'instant'}})"); pg.wait_for_timeout(150)
        pg.wait_for_timeout(1500)
    for label_,kw,block in (('normal',dict(reduced_motion='no-preference'),False),('reduced-motion',dict(reduced_motion='reduce'),False),('GSAP blocked',dict(reduced_motion='no-preference'),True),('JS disabled',dict(java_script_enabled=False),False)):
        ctx=b.new_context(viewport={'width':1024,'height':800},**kw)
        if block: ctx.route('**/vendor/gsap/**',lambda r:r.abort())
        pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(800)
        if kw.get('java_script_enabled') is False:
            r=pg.evaluate("()=>1") if False else None
            cnt=pg.locator('#team .roster > li').count(); fc=pg.locator('#team .member-card').count()
            vis=all(pg.locator('#team .roster > li').nth(i).is_visible() for i in range(cnt))
            chk(f'6.4 {label_}: all 21 roster entries + 4 featured cards present and visible',cnt==21 and fc==4 and vis,(cnt,fc,vis))
        else:
            scroll_team(pg); v=pg.evaluate(VIS)
            chk(f'6.4 {label_}: after settling, everything visible (opacity 1), 21 + 4 present',v['hidden']==0 and v['roster']==21 and v['feat']==4,v)
            chk(f'6.4 {label_}: js-motion class '+('set' if label_=='normal' else 'absent'),v['motion']==(label_=='normal'),v['motion'])
            leftover=pg.evaluate("[...document.querySelectorAll('#team .member-card,#team .roster-panel,#team .team__head > *')].filter(e=>e.style.transform||e.style.opacity).length")
            chk(f'6.4 {label_}: no leftover inline transform/opacity after the entrance',leftover==0,leftover)
        ctx.close()
    ctx=b.new_context(viewport={'width':1024,'height':800}); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(800)
    pg.evaluate("document.getElementById('team').scrollIntoView({behavior:'instant'})"); pg.wait_for_timeout(1500)
    chk('6.4 keyboard: no focusable controls inside featured cards or roster (nothing dead to tab to)',pg.evaluate("document.querySelectorAll('#team .team__featured a,#team .team__featured button,#team .roster a,#team .roster button,#team [tabindex]:not([tabindex=\"-1\"])').length")==0)
    pg.focus('header a[href="#team"]'); 
    for _ in range(3): pg.keyboard.press('Tab')
    chk('6.4 keyboard: tabbing from the Team nav link never lands on a hidden/inert element',pg.evaluate("(()=>{const a=document.activeElement;if(!a)return false;const r=a.getBoundingClientRect();return getComputedStyle(a).visibility!=='hidden'})()"))
    ctx.close()
    # CLS across the Team section while it animates in
    ctx=b.new_context(viewport={'width':390,'height':800}); pg=ctx.new_page()
    pg.add_init_script("window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:'layout-shift',buffered:true});")
    pg.goto(URL); pg.wait_for_timeout(800); scroll_team(pg)
    cls=pg.evaluate("window.__cls"); chk('6.4 team entrance causes no layout shift beyond CLS 0.01 (page-wide)',cls<0.01,cls); ctx.close()
    b.close()
finally:
  srv.kill()
json.dump(out,open(os.path.join(root,'docs','phase6-results.json'),'w'),indent=1,ensure_ascii=False)
print(f"\n{len(out)-len(fails)}/{len(out)} passed"); sys.exit(1 if fails else 0)
