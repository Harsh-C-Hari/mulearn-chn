#!/usr/bin/env python3
"""Phase 2.6: WCAG 2.2 focus checks axe can't do: focus-not-obscured (2.4.11), focus-ring contrast (1.4.11), skip link.
Run via: AUDIT_URL=http://localhost:8765/styleguide.html python3 scripts/audit_focus.py (see run_audit.sh)"""
import os,json,asyncio
from playwright.async_api import async_playwright
URL=os.environ['AUDIT_URL']
JS='''()=>{
 const lum=c=>{const [r,g,b]=c.map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b};
 const cr=(a,b)=>{const l1=lum(a),l2=lum(b);return (Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05)};
 const parse=s=>{const m=s.match(/[\\d.]+/g).map(Number);return m.slice(0,3)};
 const e=document.activeElement;if(!e||e===document.body||e.dataset.f)return {dup:1};e.dataset.f=1;
 const cs=getComputedStyle(e);const r=e.getBoundingClientRect();
 // background: walk up to first non-transparent bg
 let bg=null,n=(parseFloat(cs.outlineOffset)>0?e.parentElement:e);while(n){const c=getComputedStyle(n).backgroundColor;const m=c.match(/[\\d.]+/g);if(m&&(m.length===3||+m[3]>0.99)){bg=parse(c);break}n=n.parentElement}
 bg=bg||[248,243,233];
 const oc=parse(cs.outlineColor);
 // obscured: element at its centre / top-left corner is not the element or descendant
 const pts=[[r.left+r.width/2,r.top+r.height/2],[r.left+4,r.top+4]];
 let obscured=false,by='';for(const [x,y] of pts){if(x<0||y<0||x>innerWidth||y>innerHeight)continue;const t=document.elementFromPoint(x,y);if(t&&!e.contains(t)&&!t.contains(e)){obscured=true;by=(t.className||t.tagName)+''}}
 return {k:(e.textContent||e.getAttribute('aria-label')||e.tagName).trim().slice(0,28),ring:+cr(oc,bg).toFixed(2),outline:cs.outlineWidth+' '+cs.outlineStyle,obscured,by,top:Math.round(r.top)}}'''
async def main():
    out={}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,h in [(1440,900),(390,800)]:
            pg=await b.new_page(viewport={'width':w,'height':h});await pg.goto(URL);await pg.wait_for_timeout(800)
            rows=[]
            for i in range(120):
                await pg.keyboard.press('Tab');await pg.wait_for_timeout(15)
                r=await pg.evaluate(JS)
                if r.get('dup'):break
                rows.append(r)
            low=[r for r in rows if r['ring']<3];obs=[r for r in rows if r['obscured']]
            out[w]={'stops':len(rows),'ringContrastMin':min(r['ring'] for r in rows),'ringBelow3':low[:8],'obscured':obs[:8]}
            await pg.close()
        # skip link
        pg=await b.new_page(viewport={'width':1440,'height':900});await pg.goto(URL);await pg.keyboard.press('Tab')
        first=await pg.evaluate("({t:document.activeElement.textContent.trim(),href:document.activeElement.getAttribute('href')})")
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(200)
        out['skip']={'first':first,'hash':await pg.evaluate('location.hash'),'targetExists':await pg.evaluate("!!document.querySelector(location.hash||'#none')")}
        await b.close()
    json.dump(out,open('docs/audit-focus.json','w'),indent=1);print(json.dumps(out,indent=1))
asyncio.run(main())
