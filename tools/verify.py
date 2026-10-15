from playwright.sync_api import sync_playwright
from pathlib import Path
import json
base='http://127.0.0.1:8765/KINETONE/'
# For local document root at docs, relative base /KINETONE/ requires mirroring the path.
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading
class H(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  if path.startswith('/KINETONE/'):
   path=path[len('/KINETONE/'):]
  return super().translate_path('/'+path.lstrip('/'))
 def log_message(self,*args):pass
import os
os.chdir(str(Path(__file__).resolve().parents[1]/'docs'))
srv=ThreadingHTTPServer(('127.0.0.1',8884),H);threading.Thread(target=srv.serve_forever,daemon=True).start();base='http://127.0.0.1:8884/KINETONE/'
routes=['','instruments/','instruments/pulse/','instruments/form/','instruments/loop/','play/','sessions/','journal/','design-story/','sound-story/','about/','support/']
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for width,height in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  fails=[];page.on('response',lambda r:fails.append((r.status,r.url)) if r.status>=400 else None)
  for route in routes:
   page.goto(base+route,wait_until='domcontentloaded')
   page.wait_for_timeout(110)
   doc=page.locator('main#main')
   assert doc.count()==1,(route,'missing main')
   assert page.title().endswith('KINETONE'),route
   overflow=page.evaluate('document.documentElement.scrollWidth-innerWidth')
   if overflow>5:print('OVERFLOW',width,route,overflow)
   imgs=page.locator('img')
   broken=imgs.evaluate_all('(imgs)=>imgs.filter(x=>x.complete&&x.naturalWidth===0).map(x=>x.src)')
   if broken: print('BROKEN',route,broken[:4])
   if width==1440 and route=='':page.screenshot(path='/mnt/data/kinetone-desktop.png',full_page=True)
   if width==390 and route=='':page.screenshot(path='/mnt/data/kinetone-mobile.png',full_page=True)
   if route=='play/':
    page.locator('#drum-play').click();page.wait_for_timeout(350);assert page.locator('#drum-play').inner_text()=='■ STOP';page.locator('#drum-play').click()
    page.locator('[data-instrument="form"]').click();page.locator('#synth-keys button').first.click();assert page.locator('#app-form').is_visible()
    page.locator('[data-instrument="loop"]').click();page.locator('#sampler-demo').click();assert 'SAMPLE' in page.locator('#sampler-duration').inner_text();page.locator('#sampler-play').click();page.locator('#sampler-stop').click()
    if width==1440:page.screenshot(path='/mnt/data/kinetone-play.png',full_page=True)
   if route=='sessions/':
    page.locator('[data-session="spark"]').click();page.wait_for_timeout(250);assert page.locator('[data-session="spark"]').get_attribute('aria-pressed')=='true';page.locator('[data-session="spark"]').click()
  print('VIEWPORT',width,'JS ERRORS',len(errors),'HTTP ERRORS',len(fails));print('ERRS',errors[:5]);print('FAILS',fails[:5])
  page.close()
 browser.close()
srv.shutdown()
