"""Launch Ripple Map locally using Python's built-in HTTP server (no packages)."""
import os
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parent
os.chdir(ROOT)
class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print('%s - %s' % (self.address_string(),format%args))

try:
    httpd=ThreadingHTTPServer(('127.0.0.1',0),Handler)
except OSError as e:
    print('Could not start the local server:',e,file=sys.stderr)
    sys.exit(1)
url=f'http://127.0.0.1:{httpd.server_port}/'
print('Ripple Map local preview:',url)
print('Press Ctrl+C here to stop. Your work is stored locally in your browser.')
threading.Timer(.6,lambda:webbrowser.open(url)).start()
try:httpd.serve_forever()
except KeyboardInterrupt:pass
finally:httpd.server_close()
