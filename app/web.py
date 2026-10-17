"""Local-only browser dashboard, no third-party dependencies."""
import json, os, secrets
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
from . import core

ROOT=Path(__file__).resolve().parent.parent
TOKEN=secrets.token_urlsafe(24)

class Handler(BaseHTTPRequestHandler):
 def _send(self,status,payload,content_type='application/json; charset=utf-8'):
  data=payload if isinstance(payload,bytes) else json.dumps(payload).encode()
  self.send_response(status);self.send_header('Content-Type',content_type);self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'");self.end_headers();self.wfile.write(data)
 def do_GET(self):
  path=urlparse(self.path).path
  if path=='/':return self._send(200,(ROOT/'web'/'index.html').read_bytes(),'text/html; charset=utf-8')
  if path=='/app.js':return self._send(200,(ROOT/'web'/'app.js').read_bytes(),'text/javascript; charset=utf-8')
  if path=='/api/data':
   with core.connect() as c:
    accounts=[dict(x) for x in c.execute('SELECT * FROM accounts ORDER BY id DESC')]
    tasks=[dict(x) for x in c.execute('SELECT tasks.*,accounts.brand FROM tasks JOIN accounts ON accounts.id=tasks.account_id ORDER BY tasks.id DESC')]
    events=[dict(x) for x in c.execute('SELECT * FROM events ORDER BY id DESC LIMIT 100')]
   for a in accounts:
    a['email']='[REDACTED]' if a['email'] else ''
    a['phone']='[REDACTED]' if a['phone'] else ''
    a['vault_password_ref']='[REDACTED]' if a['vault_password_ref'] else ''
    a['vault_backup_ref']='[REDACTED]' if a['vault_backup_ref'] else ''
   return self._send(200,{'accounts':accounts,'tasks':tasks,'events':events,'csrf':TOKEN})
  return self._send(404,{'error':'Not found'})
 def do_POST(self):
  path=urlparse(self.path).path
  try:
   if self.headers.get('X-CSRF-Token')!=TOKEN:raise PermissionError('Invalid local session token')
   length=int(self.headers.get('Content-Length','0'))
   if length<0 or length>16384:raise ValueError('Request too large')
   data=json.loads(self.rfile.read(length))
   if not isinstance(data,dict):raise ValueError('Expected object')
   if path=='/api/accounts':
    brand=str(data['brand']).strip();owner=str(data['owner']).strip();handle=str(data.get('handle','')).strip()
    if not brand or not owner or len(brand)>100 or len(owner)>100 or len(handle)>100:raise ValueError('Invalid account details')
    result=core.register(brand,owner,handle)
   elif path=='/api/tasks':
    kind=str(data['kind']).strip();owner=str(data['owner']).strip();days=int(data.get('days',1))
    if not kind or not owner or len(kind)>100 or len(owner)>100 or not 0<=days<=365:raise ValueError('Invalid task details')
    result=core.task(int(data['account_id']),kind,owner,days)
   elif path=='/api/tasks/complete':
    core.complete(int(data['task_id']),str(data.get('notes','Human-confirmed')));result={'ok':True}
   elif path=='/api/accounts/status':
    core.update(int(data['account_id']),status=str(data['status']));result={'ok':True}
   elif path=='/api/audit':result={'findings':core.audit()}
   elif path=='/api/reminders':result={'reminders':core.reminders()}
   else:return self._send(404,{'error':'Not found'})
   return self._send(200,result)
  except (ValueError,KeyError,TypeError,PermissionError) as exc:return self._send(400,{'error':str(exc)})
  except Exception:
   self.log_error('Internal error');return self._send(500,{'error':'Internal server error'})

def main():
 os.chdir(ROOT)
 os.environ.setdefault('OPS_DB',str(ROOT/'ops.db'))
 core.init()
 server=ThreadingHTTPServer(('127.0.0.1',8000),Handler)
 print('GAJAN local dashboard: http://localhost:8000 (Ctrl+C to stop)',flush=True)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.server_close()
if __name__=='__main__':main()
