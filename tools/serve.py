"""Serve /KINETONE/... routes on localhost, as on GitHub Pages."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parents[1]/'docs')
class Handler(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  if path.startswith('/KINETONE/'):
   path=path[len('/KINETONE/'):]
  return super().translate_path('/'+path.lstrip('/'))
if __name__=='__main__':
 print('Open http://localhost:8073/KINETONE/')
 ThreadingHTTPServer(('127.0.0.1',8073),Handler).serve_forever()
