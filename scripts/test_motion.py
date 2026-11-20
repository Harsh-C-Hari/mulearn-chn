#!/usr/bin/env python3
"""Verify the motion-guard contract in headless Chromium (3 scenarios).
   A normal visitor · reduced-motion visitor · GSAP blocked (simulated failure).
   Usage: python3 scripts/test_motion.py [page.html]   (default docs/decor-sheet.html)"""
import sys, os, json, asyncio
from playwright.async_api import async_playwright
page_path = sys.argv[1] if len(sys.argv) > 1 else "docs/decor-sheet.html"
URL = "file://" + os.path.abspath(page_path)
async def scenario(b, name, reduced=False, block_gsap=False):
    ctx = await b.new_context(reduced_motion="reduce" if reduced else "no-preference", viewport={"width":1280,"height":800})
    pg = await ctx.new_page(); errs=[]; reqs=[]
    pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("request", lambda r: reqs.append(r.url))
    if block_gsap: await pg.route("**/vendor/gsap/**", lambda r: r.abort())
    await pg.goto(URL); await pg.wait_for_timeout(700)
    r = await pg.evaluate("""()=>({jsClass:document.documentElement.classList.contains('js'),
      motionClass:document.documentElement.classList.contains('js-motion'),
      ready:!!(window.MULEARN&&MULEARN.motion&&MULEARN.motion.ready),
      reduced:MULEARN.motion.reduced, gsap:typeof window.gsap, st:typeof window.ScrollTrigger,
      version:window.gsap&&gsap.version,
      hiddenEls:[...document.querySelectorAll('body *')].filter(e=>{const s=getComputedStyle(e);return s.visibility==='hidden'&&!e.closest('svg')&&!e.closest('[hidden]')}).length})""")
    ext=[u for u in reqs if not u.startswith(("file://","data:")) ]
    gs=[u.rsplit('/',1)[-1] for u in reqs if "vendor/gsap" in u]
    await ctx.close()
    return {name:{**r,"consoleErrors":errs,"externalRequests":ext,"gsapRequests":gs}}
async def main():
    out={}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        out.update(await scenario(b,"normal"))
        out.update(await scenario(b,"reduced_motion",reduced=True))
        out.update(await scenario(b,"gsap_blocked",block_gsap=True))
        await b.close()
    print(json.dumps(out,indent=1))
    n,r,g=out["normal"],out["reduced_motion"],out["gsap_blocked"]
    ok = (n["ready"] and n["motionClass"] and n["gsap"]=="object" and n["st"] in ("object","function") and
          not r["ready"] and not r["motionClass"] and r["gsap"]=="undefined" and r["gsapRequests"]==[] and
          not g["ready"] and not g["motionClass"] and g["hiddenEls"]==0 and
          all(not x["externalRequests"] and not x["consoleErrors"] for x in (n,r)) and not g["externalRequests"])
    print("\nRESULT:", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
asyncio.run(main())
