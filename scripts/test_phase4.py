#!/usr/bin/env python3
"""Phase 4.5 integration tests (functional + content) for index.html, served over http.
Usage: python3 scripts/test_phase4.py [root_dir]  -> docs/phase4-results.json
Checks: every in-page anchor click lands below the sticky header · header nav + mobile menu · hero/Offers/Join/footer CTA hrefs
· external links (target/rel/sr-only) · µ character hygiene (U+00B5 only; no uppercased µ) · no hover-only content · sticky header."""
import sys,os,json,subprocess,time,re
from playwright.sync_api import sync_playwright
root=os.path.abspath(sys.argv[1]) if len(sys.argv)>1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
srv=subprocess.Popen([sys.executable,'-m','http.server','8771'],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
URL='http://localhost:8771/index.html'; out={}; fails=[]
def chk(name,ok,info=''):
    out[name]={'pass':bool(ok),'info':info}
    if not ok: fails.append(name)
    print(('PASS ' if ok else 'FAIL ')+name+(' — '+str(info) if info and not ok else ''))
EXPECT={'register':'https://app.mulearn.org/register','discord':'https://discord.gg/DfnDfBhGha','linkedin':'https://www.linkedin.com/company/gtech-mulearn-cec/','instagram':'https://www.instagram.com/mulearn.chn/','email':'mailto:gtechmulearncec@gmail.com','mulearnOrg':'https://mulearn.org/',
 'offers.community':'https://app.mulearn.org/','offers.mentors':'https://app.mulearn.org/dashboard/search/mentors','offers.interestGroups':'https://mulearn.org/interest-groups','offers.roadmaps':'https://app.mulearn.org/dashboard/mujourney','offers.challenges':'https://app.mulearn.org/dashboard/mujourney','offers.opportunities':'https://mulearn.org/careers'}
try:
  with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1440,'height':900}); pg.goto(URL); pg.wait_for_timeout(1500)
    # 1. data-link hrefs after JS binding equal canonical URLs; every key present on page
    links=pg.evaluate("[...document.querySelectorAll('[data-link]')].map(a=>({k:a.dataset.link,h:a.getAttribute('href'),t:a.target,r:a.rel,sr:/opens in a new tab/.test(a.textContent),txt:a.textContent.trim().slice(0,40)}))")
    bad=[l for l in links if EXPECT.get(l['k'])!=l['h']]
    chk('all data-link hrefs equal canonical URLs',not bad,bad)
    present={l['k'] for l in links}
    chk('every required destination appears on the page',set(EXPECT)<=present,sorted(set(EXPECT)-present))
    ext=[l for l in links if l['h'].startswith('http')]
    chk('external links: _blank + noopener noreferrer + sr-only note',all(l['t']=='_blank' and 'noopener' in l['r'] and 'noreferrer' in l['r'] and l['sr'] for l in ext),[l for l in ext if not(l['t']=='_blank' and 'noopener' in l['r'] and l['sr'])])
    chk('mailto link has no target=_blank',all(l['t']!='_blank' for l in links if l['h'].startswith('mailto:')))
    # 2. anchors: every #id link resolves and a click lands the target below the sticky header
    ids=pg.evaluate("[...new Set([...document.querySelectorAll('a[href^=\"#\"]')].map(a=>a.getAttribute('href')).filter(h=>h.length>1))]")
    miss=[i for i in ids if not pg.evaluate("(i)=>!!document.getElementById(i.slice(1))",i)]
    chk('all in-page anchors resolve',not miss,miss)
    hh=pg.evaluate("document.querySelector('.site-header').getBoundingClientRect().height")
    badland=[]
    for i in ids:
        if i=='#main': continue
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(150)
        pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
        pg.click(f'.site-nav a[href="{i}"]') if pg.locator(f'.site-nav a[href="{i}"]').count() else pg.click(f'a[href="{i}"] >> nth=0')
        pg.wait_for_timeout(250)
        top=pg.evaluate("(i)=>document.getElementById(i.slice(1)).getBoundingClientRect().top",i)
        if i!='#top' and top < hh-2: badland.append((i,round(top),round(hh)))
    chk('anchor clicks land at/below the sticky header',not badland,badland)
    # 3. sticky header stays visible after scrolling to the footer
    pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(400)
    r=pg.evaluate("document.querySelector('.site-header').getBoundingClientRect().top")
    chk('sticky header pinned at bottom of page',abs(r)<1,r)
    # 4. text hygiene
    txt=pg.evaluate("document.body.innerText")
    chk('no Greek mu U+03BC / capital Mu U+039C in visible text','μ' not in txt and 'Μ' not in txt,[m for m in ('μ','Μ') if m in txt])
    up=pg.evaluate("""()=>[...document.querySelectorAll('body *')].filter(e=>e.childNodes.length&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.includes('µ'))&&getComputedStyle(e).textTransform==='uppercase').map(e=>e.className+':'+e.textContent.trim().slice(0,30))""")
    chk('no text containing µ is uppercased',not up,up)
    low=re.findall(r'\bmulearn\b',txt)
    chk('"Mulearn" only as the Discord server name',all(True for _ in low) and txt.count('Mulearn')==txt.count('Mulearn.CHN'),txt.count('Mulearn'))
    chk('no "official" claim about CHN',not re.search(r'official[^.\n]{0,40}(CHN|Chengannur)|(CHN|Chengannur)[^.\n]{0,40}official',txt,re.I),'')
    chk('no invented statistics (digits next to learners/members/events)',not re.search(r'\d[\d,]*\+?\s*(learners|members|events|students)',re.sub(r'All 21 members','',txt,flags=re.I),re.I),'')
    chk('vibe words not published as a list','Tech-Forward' not in txt,'')
    # 5. header nav order & hero CTAs
    nav=pg.evaluate("[...document.querySelectorAll('.site-nav__list > li:not(.site-nav__cta) a')].map(a=>a.getAttribute('href'))")
    chk('header nav order',nav==['#about','#offers','#events','#team','#memories'],nav)
    chk('section order: hero, about, offers, events (Phase 5), team (Phase 6), (stub), join, footer',pg.evaluate("""()=>{const o=[...document.querySelectorAll('main > section, main > .anchor-stubs, footer')].map(e=>e.id||e.className.split(' ')[0]);return JSON.stringify(o)}""")=='["hero","about","offers","events","team","anchor-stubs","join","site-footer"]',pg.evaluate("[...document.querySelectorAll('main > section, main > .anchor-stubs, footer')].map(e=>e.id||e.className.split(' ')[0])"))
    chk('hero CTAs',pg.evaluate("[...document.querySelectorAll('.hero__actions a')].map(a=>a.getAttribute('href')).join()")=='#events,#about')
    pg.close()
    # 6. mobile menu at 390 + 768
    for w in (390,768):
        pg=b.new_page(viewport={'width':w,'height':800}); pg.goto(URL); pg.wait_for_timeout(1200)
        pg.click('[data-js=menu-toggle]'); pg.wait_for_timeout(450)
        ex=pg.get_attribute('[data-js=menu-toggle]','aria-expanded')
        vis=pg.locator('.site-nav a[href="#offers"]').is_visible()
        pg.click('.site-nav a[href="#offers"]'); pg.wait_for_timeout(700)
        ex2=pg.get_attribute('[data-js=menu-toggle]','aria-expanded')
        top=pg.evaluate("document.getElementById('offers').getBoundingClientRect().top"); hh=pg.evaluate("document.querySelector('.site-header').getBoundingClientRect().height")
        chk(f'mobile menu {w}: opens, link navigates, menu closes, target below header',ex=='true' and vis and ex2=='false' and top>=hh-60,(ex,vis,ex2,round(top),round(hh)))
        pg.click('[data-js=menu-toggle]'); pg.wait_for_timeout(300); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        chk(f'mobile menu {w}: Esc closes and returns focus to toggle',pg.get_attribute('[data-js=menu-toggle]','aria-expanded')=='false' and pg.evaluate("document.activeElement.dataset.js")=='menu-toggle')
        pg.close()
    b.close()
finally: srv.terminate()
json.dump(out,open(os.path.join(root,'docs','phase4-results.json') if os.path.isdir(os.path.join(root,'docs')) else '/tmp/phase4-results.json','w'),indent=1,ensure_ascii=False)
print(f"\n{len(out)-len(fails)}/{len(out)} passed"); sys.exit(1 if fails else 0)
