#!/usr/bin/env python3
"""Shared helpers for skeleton tests. Serves the project over http://127.0.0.1 and lets a test hold, delay,
fail or pass image requests (route interception) so every skeleton state can be observed deterministically."""
import os, threading, http.server, socketserver, functools, time
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
def serve(port=0):
    h=functools.partial(Q,directory=ROOT)
    s=socketserver.ThreadingTCPServer(('127.0.0.1',port),h); s.daemon_threads=True
    threading.Thread(target=s.serve_forever,daemon=True).start()
    return s,f'http://127.0.0.1:{s.server_address[1]}'
IMG='**/img/**'
def hold(page):
    """image requests stay pending -> skeletons stay. Use release(page) (or close_page) before closing."""
    page._held=[]
    page.route(IMG,lambda r: page._held.append(r))
def release(page,mode='continue'):
    """let every held image through ('continue') or fail them ('abort')"""
    for r in list(getattr(page,'_held',[])):
        try: (r.continue_() if mode=='continue' else r.abort())
        except Exception: pass
    page._held=[]
def close_page(page):
    release(page,'abort')
    try: page.unroute_all(behavior='ignore_errors')
    except Exception: pass
    page.close()
def fail(page):
    page.route(IMG,lambda r: r.abort())
def delay(page,ms):
    def h(r):
        time.sleep(ms/1000); 
        try: r.continue_()
        except Exception: pass
    page.route(IMG,h)
