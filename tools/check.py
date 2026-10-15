"""Dependency-free verification for the built KINETONE website."""
from pathlib import Path
from html.parser import HTMLParser
import re, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
EXPECTED=['','instruments/','instruments/pulse/','instruments/form/','instruments/loop/','play/','sessions/','journal/','design-story/','sound-story/','about/','support/']
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.urls=[];self.title=False;self.main=False;self.images=[];self.ids=set();self.duplicates=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='main':self.main=True
  if tag=='img':self.images.append(d)
  if d.get('id'):
   if d['id'] in self.ids:self.duplicates.append(d['id'])
   self.ids.add(d['id'])
  for attr in ('href','src'):
   if d.get(attr):self.urls.append(d[attr])
for route in EXPECTED:
 path=DOCS/route/'index.html' if route else DOCS/'index.html'
 assert path.exists(),str(path)
 parser=Parser();parser.feed(path.read_text(encoding='utf8'))
 assert parser.main, f'No main: {route}'
 assert not parser.duplicates, f'Duplicate IDs {route}: {parser.duplicates}'
 for url in parser.urls:
  if url.startswith('/KINETONE/'):
   clean=url.split('#')[0].split('?')[0][10:]
   dest=DOCS/clean
   assert dest.is_file() or (dest/'index.html').is_file(),f'Broken internal link: {route} -> {url}'
 for img in parser.images:
  assert img.get('alt') is not None, f'Missing alt: {route}'
 assert 'KINETONE' in path.read_text(encoding='utf8'),f'No title: {route}'
images=list((DOCS/'assets/img').glob('*.webp'))
assert len(images)==28,f'{len(images)} images instead of 28'
assert len(set(i.name for i in images))==28
assert all(i.stat().st_size>10_000 for i in images)
js=DOCS/'assets/site.js';assert js.exists()
result=subprocess.run(['node','--check',str(js)],capture_output=True,text=True)
assert result.returncode==0,result.stderr
css=(DOCS/'assets/site.css').read_text()
assert css.count('{')==css.count('}'),'Unbalanced CSS'
assert all(x in (DOCS/'play/index.html').read_text() for x in ['id="pad-grid"','id="synth-keys"','id="sampler-record"']), 'Missing playable controls'
print('PASS:',len(EXPECTED),'pages,',len(images),'photographs, internal links, image alternative text, unique element IDs, JS syntax, and playable instrument controls')
