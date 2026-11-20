#!/usr/bin/env python3
"""Phase 2.6 audit: axe-core (WCAG 2.2 AA), overflow, keyboard/focus, reduced-motion, fonts, GSAP, console, network.
Usage: python3 scripts/audit_a11y.py [html] [axe.min.js path] -> writes docs/audit-results.json
axe-core is a dev-only tool and is NOT shipped in the site."""
import sys,os,json,asyncio
from playwright.async_api import async_playwright
HTML=sys.argv[1] if len(sys.argv)>1 else 'styleguide.html'
AXE=sys.argv[2] if len(sys.argv)>2 else '/tmp/axe/node_modules/axe-core/axe.min.js'
URL=os.environ.get("AUDIT_URL") or "file://"+os.path.abspath(HTML)
W=[320,390,768,1024,1440]
async def main():
    out={}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        # --- per width: overflow, console, network, axe
        for w in W:
            pg=await b.new_page(viewport={'width':w,'height':900})
            errs=[];reqs=[]
            pg.on('console',lambda m,e=errs:e.append(m.text) if m.type in('error','warning') else None)
            pg.on('pageerror',lambda e,x=errs:x.append(str(e)))
            pg.on('request',lambda r,q=reqs:q.append(r.url))
            await pg.goto(URL);await pg.wait_for_timeout(2600)  # let entrance animations finish (3.5)
            await pg.evaluate('document.fonts.ready')
            m=await pg.evaluate('({sw:document.documentElement.scrollWidth,iw:innerWidth})')
            await pg.add_script_tag(path=AXE)
            ax=await pg.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}})")
            viol=[{'id':v['id'],'impact':v['impact'],'n':len(v['nodes']),'help':v['help'],'targets':[n['target'] for n in v['nodes'][:4]]} for v in ax['violations']]
            from urllib.parse import urlparse
            base=urlparse(URL);ext=[r for r in reqs if not r.startswith(('file://','data:')) and urlparse(r).netloc!=base.netloc]
            # tap targets for interactive controls
            small=await pg.evaluate('''()=>{const o=[];document.querySelectorAll('a[href],button,input,select,textarea,[tabindex="0"]').forEach(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);if(!r.width||cs.visibility==='hidden')return;if(e.closest('p,li,.prose')&&e.tagName==='A'&&cs.display==='inline')return;if(r.height<24||r.width<24)o.push((e.className||e.tagName)+' '+Math.round(r.width)+'x'+Math.round(r.height))});return o.slice(0,10)}''')
            out[w]={'overflowX':m['sw']>m['iw'],'scrollWidth':m['sw'],'console':errs,'external':ext,'axeViolations':viol,'targetsUnder24px':small}
            await pg.close()
        # --- fonts + gsap + sematics at 1440
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(URL);await pg.wait_for_timeout(1200)
        out['fonts']=await pg.evaluate('''async()=>{await document.fonts.ready;return [...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight)}''')
        out['gsap']=await pg.evaluate('({gsap:typeof window.gsap,st:typeof window.ScrollTrigger,ver:window.gsap&&gsap.version,cls:document.documentElement.className})')
        out['semantics']=await pg.evaluate('''()=>{const hs=[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h=>+h.tagName[1]);let skips=0;for(let i=1;i<hs.length;i++)if(hs[i]-hs[i-1]>1)skips++;
          return {lang:document.documentElement.lang,title:document.title,h1:hs.filter(x=>x===1).length,headings:hs.length,headingSkips:skips,main:document.querySelectorAll('main').length,header:document.querySelectorAll('header').length,nav:document.querySelectorAll('nav').length,footer:document.querySelectorAll('footer').length,skipLink:!!document.querySelector('a[href^="#"].skip,.skip-link,a.skip'),imgNoAlt:[...document.images].filter(i=>!i.hasAttribute('alt')).length,viewport:!!document.querySelector('meta[name=viewport]')}}''')
        # keyboard walk
        stops=0;noFocus=[];seen=set()
        await pg.evaluate('document.activeElement&&document.activeElement.blur()')
        for i in range(160):
            await pg.keyboard.press('Tab')
            info=await pg.evaluate('''()=>{const e=document.activeElement;if(!e||e===document.body)return null;if(e.dataset.seen)return {dup:1};e.dataset.seen=1;const cs=getComputedStyle(e);const r=e.getBoundingClientRect();
              const vis=cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>=2;const sh=cs.boxShadow!=='none';
              return {k:(e.tagName+'|'+(e.id||'')+'|'+(e.getAttribute('href')||'')+'|'+(e.textContent||'').trim().slice(0,30)),vis,sh,ol:cs.outlineWidth+' '+cs.outlineStyle,w:r.width,h:r.height}}''')
            if not info: continue
            if info.get('dup'): break
            stops+=1
            if not info['vis']: noFocus.append(info['k']+' ol='+info['ol'])
        out['keyboard']={'tabStops':stops,'withoutVisibleOutline':noFocus[:15]}
        await pg.close()
        # --- reduced motion
        ctx=await b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce')
        pg=await ctx.new_page();reqs=[]
        pg.on('request',lambda r,q=reqs:q.append(r.url))
        await pg.goto(URL);await pg.wait_for_timeout(1200)
        out['reducedMotion']={'jsMotionClass':await pg.evaluate("document.documentElement.classList.contains('js-motion')"),
          'gsapLoaded':await pg.evaluate("typeof window.gsap"),'gsapRequested':[r.split('/')[-1] for r in reqs if 'gsap' in r.lower() or 'ScrollTrigger' in r],
          'maxTransitionMs':await pg.evaluate('''()=>{let m=0;document.querySelectorAll('*').forEach(e=>{const cs=getComputedStyle(e);const d=cs.transitionDuration.split(',').map(x=>parseFloat(x)*(x.includes('ms')?1:1000));const a=cs.animationDuration.split(',').map(x=>parseFloat(x)*(x.includes('ms')?1:1000));m=Math.max(m,...d,...a)});return m}''')}
        await ctx.close()
        # --- JS disabled: content visible
        ctx=await b.new_context(viewport={'width':1440,'height':900},java_script_enabled=False)
        pg=await ctx.new_page();await pg.goto(URL);await pg.wait_for_timeout(500)
        out['noJS']={'bodyTextLen':len(await pg.evaluate("document.body.innerText")),'hiddenSections':await pg.evaluate("[...document.querySelectorAll('section')].filter(s=>getComputedStyle(s).opacity==='0'||getComputedStyle(s).visibility==='hidden').length")}
        await ctx.close();await b.close()
    json.dump(out,open(os.environ.get('AUDIT_OUT','docs/audit-results.json'),'w'),indent=1)
    print(json.dumps(out,indent=1)[:9000])
asyncio.run(main())
