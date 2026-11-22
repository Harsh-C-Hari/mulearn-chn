#!/usr/bin/env python3
"""Reveal-lock verification: per-frame sampling of inline/computed transform + opacity for every element animated by motion-home.js
that carries a CSS transform transition. Usage: test_reveal_lock.py [project_dir] [out.json]"""
import sys, os, json, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright
print = functools.partial(print, flush=True)
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..'))
OUTJ = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'docs', 'reveal-lock-results.json')
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def log_message(s, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), Q); threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{srv.server_address[1]}/index.html'
GROUPS = {'hero buttons': '.hero__actions > *', 'about cards': '.about__pair .card', 'offer cards': '.offer__card',
          'featured event cards': '.event--featured .event-card', 'featured member cards': '.team__featured .member-card',
          'polaroids': '.memories__collage .polaroid', 'join CTAs': '.join__ctas > *'}
SAMPLER = """(G=>{window.__S={};const P=s=>{if(!s||s==='none')return 0;const m=s.match(/matrix(3d)?\\(([^)]+)\\)/);if(!m)return 0;const v=m[2].split(',').map(Number);return m[1]?v[13]:v[5]};
function tick(t){for(const k in G){document.querySelectorAll(G[k]).forEach((e,i)=>{const id=k+'#'+i;(window.__S[id]=window.__S[id]||[]).push([Math.round(t),e.style.transform,+P(getComputedStyle(e).transform).toFixed(2),+(+getComputedStyle(e).opacity).toFixed(3),e.classList.contains('is-revealing')?1:0,getComputedStyle(e).transform])})}requestAnimationFrame(tick)}
requestAnimationFrame(tick)})(%s)"""
res = {}; ok = True
def check(n, c, i=''):
    global ok; ok = ok and bool(c); res[n] = {'pass': bool(c), 'info': str(i)[:300]}; print(('PASS ' if c else 'FAIL ') + n, str(i)[:200])

def analyse(fr):
    # fr: [t, inline, ty, opacity, locked, computed]
    ty0 = max([f[2] for f in fr if f[3] < 0.02] + [0])
    win = [f for f in fr if 0.03 < f[3] < 0.97]
    err = max([abs(f[2] / ty0 - (1 - f[3])) for f in win] + [0]) if ty0 > 1 else None
    # reveal finished = first frame (after the element was hidden) whose inline transform has been cleared by clearProps
    hid = next((i for i, f in enumerate(fr) if f[3] < 0.5), None)
    done = next((i for i, f in enumerate(fr) if hid is not None and i > hid and f[1] == '' and f[3] >= 0.99), None)
    last = fr[-1]
    # no motion after the reveal finished: computed transform constant for the remaining frames
    post = [f[5] for f in fr[done:]] if done is not None else []
    return dict(ty0=ty0, frames=len(win), sync_err=None if err is None else round(err, 3), finished=done is not None,
                end_inline=last[1], end_locked=last[4], end_computed=last[5], settle_changes=len(set(post)) - 1 if post else None,
                locked_while_animating=all(f[4] for f in fr if 0.0 < f[3] < 0.999 or (f[3] < 0.02 and f[2] > 1)))

with sync_playwright() as p:
    b = p.chromium.launch()
    for vw, vh in ((375, 812), (1280, 800)):
        # baseline resting transforms (no GSAP: reduced motion)
        ctx = b.new_context(viewport={'width': vw, 'height': vh}, reduced_motion='reduce'); pg = ctx.new_page(); pg.goto(URL, wait_until='load'); pg.wait_for_timeout(800)
        base = {k: pg.evaluate("s=>[...document.querySelectorAll(s)].map(e=>getComputedStyle(e).transform)", sel) for k, sel in GROUPS.items()}
        locked = pg.evaluate("document.querySelectorAll('.is-revealing').length")
        inl = pg.evaluate("[...document.querySelectorAll('.hero__actions > *,.about__pair .card,.offer__card,.polaroid,.member-card,.join__ctas > *')].filter(e=>e.style.transform||e.style.opacity==='0').length")
        vis = pg.evaluate("s=>[...document.querySelectorAll(s)].every(e=>+getComputedStyle(e).opacity===1)", ','.join(GROUPS.values()))
        check(f'{vw}: reduced motion → no .is-revealing, no inline start states, all targets visible', locked == 0 and inl == 0 and vis, {'locked': locked, 'inline': inl, 'visible': vis})
        ctx.close()
        for name, sel in GROUPS.items():
            ctx = b.new_context(viewport={'width': vw, 'height': vh}); pg = ctx.new_page(); pg.set_default_timeout(15000)
            pg.add_init_script(SAMPLER % json.dumps({name: sel}))
            pg.goto(URL, wait_until='load'); pg.wait_for_timeout(1800 if name == 'hero buttons' else 600)
            n = pg.evaluate("s=>document.querySelectorAll(s).length", sel)
            if name != 'hero buttons':
                for i in range(n):
                    pg.evaluate("([s,i])=>document.querySelectorAll(s)[i].scrollIntoView({block:'center'})", [sel, i]); pg.wait_for_timeout(1300)
            pg.wait_for_timeout(900)
            S = pg.evaluate("window.__S")
            bad = []; rows = []
            for i in range(n):
                fr = S.get(f'{name}#{i}', []); a = analyse(fr); rows.append(a)
                rest = base[name][i] if i < len(base[name]) else None
                good = (a['finished'] and a['ty0'] > 1 and a['sync_err'] is not None and a['sync_err'] < 0.25 and a['end_inline'] == '' and not a['end_locked']
                        and a['end_computed'] == rest and a['settle_changes'] == 0 and a['locked_while_animating'])
                if not good: bad.append({'i': i, **a, 'rest': rest})
            check(f'{vw}: {name} ({n}) — rises in sync with the fade, no late snap, lock released, ends at CSS rest transform', n > 0 and not bad, bad[:2] or {'max_sync_err': max(r['sync_err'] or 0 for r in rows), 'ty0': sorted({r['ty0'] for r in rows})})
            if name in ('hero buttons', 'offer cards') and rows:
                fr = S[f'{name}#0']; k = [f for f in fr if 0.0 < f[3] < 0.999]
                step = max(1, len(k) // 8); res.setdefault('frame_samples', {})[f'{vw} {name}#0'] = [dict(t=f[0], inline=f[1], computed_ty=f[2], opacity=f[3], locked=f[4]) for f in k[::step][:9]]
            ctx.close()
        # hover still animates smoothly after the reveal (uses the last context logic on a fresh, fully revealed page)
        ctx = b.new_context(viewport={'width': vw, 'height': vh}); pg = ctx.new_page(); pg.set_default_timeout(15000)
        pg.goto(URL, wait_until='load'); pg.wait_for_timeout(1800)
        H = {'.btn': '.hero__actions > .btn', 'a.card': '.offer__card', '.event-card': '.event--featured .event-card', '.polaroid': '.memories__collage .polaroid'}
        for lab, sel in H.items():
            pg.evaluate("s=>document.querySelector(s).scrollIntoView({block:'center'})", sel); pg.wait_for_timeout(1800)
            pg.hover(sel); 
            vals = pg.evaluate("""async s=>{const e=document.querySelector(s),p=e.querySelector('.event-card__poster'),o=[];const t0=performance.now();
              while(performance.now()-t0<700){o.push([getComputedStyle(e).transform,p?getComputedStyle(p).transform:''].join('|'));await new Promise(r=>requestAnimationFrame(r))}return o}""", sel)
            d = len(set(vals)); check(f'{vw}: hover lift on {lab} still animates (intermediate frames, not a jump)', d >= 4, f'{d} distinct frames')
            pg.mouse.move(0, 0); pg.wait_for_timeout(400)
        ctx.close()
    b.close()
json.dump(res, open(OUTJ, 'w'), indent=1)
print('OVERALL', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
