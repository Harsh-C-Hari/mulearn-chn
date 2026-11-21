import asyncio, json, sys, os, threading, http.server, socketserver, functools

# Phase 8.2 tests: scroll motion standardisation. Usage: python3 scripts/test_phase8_scroll.py  (serves the project on 127.0.0.1)
class _srv:
    @staticmethod
    def start(root, port):
        class H(http.server.SimpleHTTPRequestHandler):
            def log_message(self,*a): pass
        socketserver.TCPServer.allow_reuse_address=True
        s=socketserver.ThreadingTCPServer(('127.0.0.1',port),functools.partial(H,directory=root))
        threading.Thread(target=s.serve_forever,daemon=True).start(); return s
srv=_srv
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); srv.start(ROOT,8766); BASE='http://127.0.0.1:8766/index.html'
HID="()=>[...document.querySelectorAll('body *')].filter(e=>{const s=e.style;return (s.opacity!==''&&+s.opacity<1)}).length"
ABOVE="()=>[...document.querySelectorAll('body *')].filter(e=>e.style.opacity==='0'&&e.getBoundingClientRect().bottom<0).length"
res=[]
def ck(name,ok,info=''):
    res.append((name,bool(ok),info)); print(('PASS ' if ok else 'FAIL ')+name, info)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    # 1 deep links land (normal motion), at 5 widths
    for w,h in((320,640),(390,800),(768,1024),(1024,768),(1440,900)):
        for hsh in('#offers','#team','#join'):
            ctx=await b.new_context(viewport={'width':w,'height':h}); pg=await ctx.new_page(); errs=[]
            pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
            await pg.goto(BASE+hsh,wait_until='load'); await pg.wait_for_timeout(2600)
            top=await pg.evaluate(f"Math.round(document.querySelector('{hsh}').getBoundingClientRect().top)")
            ck(f'deep link {hsh} @{w}', -2<=top<=130, f'top={top}')
            ck(f'  nothing hidden above viewport @{w}{hsh}', await pg.evaluate(ABOVE)==0)
            ck(f'  no console errors @{w}{hsh}', not errs, str(errs))
            await ctx.close()
    # 2 hero: no visible->hidden flash. sample opacity of title spans from first frame
    for w in (390,1440):
        ctx=await b.new_context(viewport={'width':w,'height':900}); pg=await ctx.new_page()
        await pg.add_init_script("window.__t=[];(function poll(){const e=document.querySelector('.hero__title span');if(e)__t.push([Math.round(performance.now()),+getComputedStyle(e).opacity]);requestAnimationFrame(poll)})()")
        await pg.goto(BASE,wait_until='load'); await pg.wait_for_timeout(3000)
        t=await pg.evaluate('__t'); 
        # flash = a visible (1) sample followed later by a lower sample
        seen1=False; flash=False
        for ms,o in t:
            if o==1: seen1=True
            elif seen1 and o<0.99: flash=True; break
        ck(f'hero has no visible→hidden flash @{w}',not flash, f'first={t[0] if t else None}')
        ck(f'hero fully visible at end @{w}', t[-1][1]==1)
        await ctx.close()
    # 3 hero release when GSAP is slow: block gsap for 1.6s -> hero visible by ~1.3s, no later re-hide
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page()
    async def slow(route):
        await asyncio.sleep(1.8); await route.continue_()
    await pg.route('**/vendor/gsap/**',slow)
    await pg.add_init_script("window.__t=[];(function poll(){const e=document.querySelector('.hero__title span');if(e)__t.push([Math.round(performance.now()),+getComputedStyle(e).opacity]);requestAnimationFrame(poll)})()")
    await pg.goto(BASE,wait_until='load'); await pg.wait_for_timeout(4500)
    t=await pg.evaluate('__t'); first1=next((m for m,o in t if o==1),None)
    later=[o for m,o in t if first1 and m>first1 and o<0.99]
    ck('slow GSAP: hero visible by ~1.4s', first1 is not None and first1<1500, f'firstVisible={first1}ms')
    ck('slow GSAP: hero not re-hidden after release', not later)
    await ctx.close()
    # 4 reduced motion + gsap blocked + JS off: everything visible, no pre-motion
    for name,kw,blk,js in(('reduced',{'reduced_motion':'reduce'},False,True),('gsap blocked',{},True,True),('js off',{},False,False)):
        ctx=await b.new_context(viewport={'width':390,'height':800},java_script_enabled=js,**kw); pg=await ctx.new_page()
        if blk: await pg.route('**/vendor/gsap/**',lambda r:r.abort())
        await pg.goto(BASE); await pg.wait_for_timeout(2500)
        vis=await pg.evaluate("[...document.querySelectorAll('.hero__title span,.about__card,.offer__card,.join__banner,.footer__big span')].every(e=>+getComputedStyle(e).opacity===1)")
        pm=await pg.evaluate("document.documentElement.classList.contains('pre-motion')")
        ck(f'{name}: content visible, no pre-motion class', vis and not pm, f'vis={vis} pm={pm}')
        await ctx.close()
    # 5 rapid scroll, then every element revealed + no leftover inline styles after settling
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page()
    await pg.goto(BASE); await pg.wait_for_timeout(2000)
    H=await pg.evaluate('document.documentElement.scrollHeight')
    for y in list(range(0,H,1500))+[H,0,H]:
        await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(25)
    await pg.wait_for_timeout(3200)
    left=await pg.evaluate("[...document.querySelectorAll('body *')].filter(e=>(e.style.opacity||e.style.transform||e.style.visibility)&&!e.matches('svg.icon')).length")
    ck('rapid scroll: no stuck/leftover inline styles', left==0, f'left={left}')
    ck('rapid scroll: all ScrollTriggers consumed', await pg.evaluate('ScrollTrigger.getAll().length')==0)
    await ctx.close()
    # 6 drawer refresh keeps join trigger accurate and does not cancel smooth scroll
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page()
    await pg.goto(BASE); await pg.wait_for_timeout(2000)
    st=lambda: pg.evaluate("Math.round(ScrollTrigger.getAll().find(t=>t.trigger&&t.trigger.classList.contains('site-footer')).start)")
    before=await st()
    await pg.evaluate("document.getElementById('memories-gallery-toggle').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(600)
    await pg.click('#memories-gallery-toggle'); await pg.wait_for_timeout(1500)
    after=await st(); jt=await pg.evaluate("Math.round(document.getElementById('join').getBoundingClientRect().top+scrollY)")
    ck('drawer open: footer trigger re-measured', after>before+1500 and abs(after-(await pg.evaluate("Math.round(document.querySelector('.site-footer').getBoundingClientRect().top+scrollY)")-900*0.92))<80, f'before={before} after={after} joinTop={jt}')
    dt=await pg.evaluate("Math.round(document.getElementById('memories-gallery').getBoundingClientRect().top)")
    ck('drawer open: smooth scroll reached the drawer', -2<=dt<=140, f'drawerTop={dt}')
    await ctx.close()
    # 7 anchor clicks smooth + hash + focus; reduced = instant; modifier click untouched; skip link native
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page()
    await pg.goto(BASE); await pg.wait_for_timeout(1800)
    await pg.evaluate("window.__s=[];addEventListener('scroll',()=>__s.push(scrollY))")
    await pg.click('.site-nav a[href="#events"]'); await pg.wait_for_timeout(2500)
    info=await pg.evaluate("({n:__s.length,top:Math.round(document.getElementById('events').getBoundingClientRect().top),hash:location.hash,focus:document.activeElement.id,cur:(document.querySelector('.site-nav [aria-current]')||{}).textContent})")
    ck('nav click: smooth (many scroll events), lands under header, hash set, target focused', info['n']>8 and 0<=info['top']<=130 and info['hash']=='#events' and info['focus']=='events', str(info))
    await pg.go_back(); await pg.wait_for_timeout(1200)
    ck('browser Back returns to previous position', await pg.evaluate('scrollY')<400, f"y={await pg.evaluate('scrollY')}")
    await pg.click('a[href="#top"]') if await pg.locator('a[href="#top"]').count() else None
    await ctx.close()
    ctx=await b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce'); pg=await ctx.new_page()
    await pg.goto(BASE); await pg.wait_for_timeout(1000)
    await pg.evaluate("window.__s=[];addEventListener('scroll',()=>__s.push(scrollY))")
    await pg.click('.site-nav a[href="#events"]'); await pg.wait_for_timeout(800)
    n=await pg.evaluate('__s.length'); top=await pg.evaluate("Math.round(document.getElementById('events').getBoundingClientRect().top)")
    ck('reduced motion: anchor jump is instant', n<=2 and 0<=top<=130, f'events={n} top={top}')
    await pg.keyboard.press('Tab'); 
    await ctx.close()
    # 8 keyboard: Enter on nav link moves and focus ring not drawn on section; next Tab continues after target
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page()
    await pg.goto(BASE); await pg.wait_for_timeout(1500)
    await pg.focus('.site-nav a[href="#team"]'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(2500)
    ring=await pg.evaluate("(()=>{const e=document.activeElement;const c=getComputedStyle(e);return [e.id,c.outlineStyle,c.boxShadow]})()")
    ck('keyboard anchor: target focused, no section ring', ring[0]=='team' and ring[1]=='none' and ring[2]=='none', str(ring))
    await pg.keyboard.press('Tab'); 
    nxt=await pg.evaluate("(()=>{const e=document.activeElement;return e.closest('#team')?'inside-team':e.tagName})()")
    ck('keyboard anchor: next Tab continues inside Team', nxt=='inside-team' or nxt!='BODY', nxt)
    await ctx.close()
    await b.close()
  bad=[r for r in res if not r[1]]
  print(f'\n{len(res)-len(bad)}/{len(res)} passed'); json.dump(res,open(os.path.join(ROOT,'docs','phase8-2-results.json'),'w'),indent=1); sys.exit(1 if bad else 0)
asyncio.run(main())
