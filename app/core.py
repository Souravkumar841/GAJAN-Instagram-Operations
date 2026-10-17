import json, sqlite3, os, re, hashlib, urllib.request, urllib.error, time
from datetime import datetime, timezone, timedelta
from pathlib import Path
DB=os.getenv('OPS_DB','ops.db')
def now(): return datetime.now(timezone.utc).isoformat()
def connect():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON');return c
def init():
 with connect() as c:
  c.executescript('''CREATE TABLE IF NOT EXISTS accounts(id INTEGER PRIMARY KEY,brand TEXT NOT NULL UNIQUE,handle TEXT,owner TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'planned',email TEXT,phone TEXT,two_factor TEXT,vault_password_ref TEXT,vault_backup_ref TEXT,profile_name TEXT,bio TEXT,link TEXT,category TEXT,image_ref TEXT,meta_business TEXT,people_roles TEXT DEFAULT '{}',blockers TEXT DEFAULT '[]',last_verified TEXT,created TEXT NOT NULL);CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY,account_id INTEGER NOT NULL,kind TEXT NOT NULL,owner TEXT NOT NULL,deadline TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'pending',notes TEXT DEFAULT '',reminders INTEGER DEFAULT 0,created TEXT NOT NULL,updated TEXT NOT NULL,UNIQUE(account_id,kind),FOREIGN KEY(account_id) REFERENCES accounts(id));CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,account_id INTEGER,action TEXT NOT NULL,detail TEXT NOT NULL,at TEXT NOT NULL);''')
def event(c,aid,action,detail):c.execute('INSERT INTO events(account_id,action,detail,at) VALUES(?,?,?,?)',(aid,action,detail,now()))
def register(brand,owner,handle=None):
 with connect() as c:
  c.execute('INSERT OR IGNORE INTO accounts(brand,owner,handle,created) VALUES(?,?,?,?)',(brand,owner,handle,now()))
  a=c.execute('SELECT * FROM accounts WHERE brand=?',(brand,)).fetchone();event(c,a['id'],'register','Idempotent registration; no Instagram signup performed');return dict(a)
def task(aid,kind,owner,days=1):
 with connect() as c:
  if not c.execute('SELECT 1 FROM accounts WHERE id=?',(aid,)).fetchone():raise ValueError('Unknown account')
  deadline=(datetime.now(timezone.utc)+timedelta(days=days)).isoformat()
  c.execute('INSERT OR IGNORE INTO tasks(account_id,kind,owner,deadline,created,updated) VALUES(?,?,?,?,?,?)',(aid,kind,owner,deadline,now(),now()))
  t=c.execute('SELECT * FROM tasks WHERE account_id=? AND kind=?',(aid,kind)).fetchone();event(c,aid,'task_created',f'{kind} task #{t["id"]} owner={owner}');return dict(t)
def safe_note(value):
 value=str(value)
 if len(value)>500: raise ValueError('Notes must be at most 500 characters')
 if re.search(r'(?i)(password|passwd|secret|token|backup.code|otp|api.key)\s*[:=]\s*\S+',value):
  raise ValueError('Do not enter credentials or codes in task notes')
 return value

def complete(tid,notes='Human-confirmed'):
 notes=safe_note(notes)
 with connect() as c:
  t=c.execute('SELECT * FROM tasks WHERE id=?',(tid,)).fetchone()
  if not t:raise ValueError('Unknown task')
  c.execute("UPDATE tasks SET status='done',notes=?,updated=? WHERE id=?",(notes,now(),tid));event(c,t['account_id'],'task_completed',f'Task {tid} completed; notes omitted for privacy')
def update(aid,**fields):
 allowed={'handle','status','email','phone','two_factor','vault_password_ref','vault_backup_ref','profile_name','bio','link','category','image_ref','meta_business','people_roles','blockers','last_verified'}
 if not fields or set(fields)-allowed:raise ValueError('Invalid fields')
 if 'status' in fields and fields['status']=='verified':raise ValueError('Use verified status only after external evidence review; this prototype cannot verify Instagram')
 if 'bio' in fields and fields['bio'] and len(fields['bio'])>150:raise ValueError('Instagram bio exceeds 150 characters')
 if 'status' in fields and fields['status'] not in {'planned','waiting_human','blocked','configured','verified'}:raise ValueError('Invalid status')
 for k in ('vault_password_ref','vault_backup_ref'):
  if k in fields and fields[k] and not re.match(r'^(vault|op|aws-sm|azure-kv)://[A-Za-z0-9_./:-]+$',fields[k]):raise ValueError('Use vault reference, never a secret')
 for k in ('people_roles','blockers'):
  if k in fields and not isinstance(fields[k],str):fields[k]=json.dumps(fields[k])
 with connect() as c:
  c.execute('UPDATE accounts SET '+','.join(f'{k}=?' for k in fields)+' WHERE id=?',(*fields.values(),aid));event(c,aid,'account_updated','Fields updated: '+','.join(fields))
def reminders():
 results=[]
 with connect() as c:
  for t in c.execute("SELECT * FROM tasks WHERE status IN ('pending','reminded','escalated')").fetchall():
   overdue=datetime.fromisoformat(t['deadline'])<datetime.now(timezone.utc)
   status='escalated' if overdue else 'reminded'
   c.execute('UPDATE tasks SET status=?,reminders=reminders+1,updated=? WHERE id=?',(status,now(),t['id']))
   event(c,t['account_id'],status,f'Task {t["id"]} owner={t["owner"]}; external delivery not configured')
   results.append({'task_id':t['id'],'owner':t['owner'],'status':status,'delivery':'queued_for_manual_delivery'})
 return results
def audit():
 findings=[]
 with connect() as c:
  accounts=c.execute('SELECT * FROM accounts').fetchall()
  for a in accounts:
   checks=[('missing_2fa',not a['two_factor']),('missing_backup_codes',not a['vault_backup_ref']),('missing_password_vault_ref',not a['vault_password_ref']),('missing_recovery_email',not a['email']),('missing_recovery_phone',not a['phone']),('stale_access_verification',not a['last_verified'] or (datetime.now(timezone.utc)-datetime.fromisoformat(a['last_verified'])).days>7)]
   for name,fail in checks:
    if fail:
     findings.append({'account_id':a['id'],'brand':a['brand'],'finding':name,'verification':'unverified','status':'open'})
     task(a['id'],'audit_'+name,a['owner'])
 return findings
def offboard(aid,person):
 with connect() as c:
  a=c.execute('SELECT * FROM accounts WHERE id=?',(aid,)).fetchone()
  if not a:raise ValueError('Unknown account')
  roles=json.loads(a['people_roles'] or '{}')
  # Do not claim Meta removal: human confirmation is required.
  assigned=person in roles
 for kind in ['remove_meta_role','rotate_accessible_credentials','replace_exposed_backup_codes','verify_access_revocation']:
  task(aid,f'offboard_{person}_{kind}',a['owner'])
 return {'person':person,'role_in_register':assigned,'completed':[],'pending':['remove Meta role','rotate accessible credentials','replace exposed backup codes','verify revocation'],'blocked':['Awaiting authorized human action / Meta access'],'verification':'unverified'}
def proxy_check(url,attempts=2,timeout=4):
 if not url.startswith('https://'):raise ValueError('Only HTTPS neutral endpoints')
 if attempts<1 or attempts>3:raise ValueError('bounded attempts 1..3')
 for n in range(attempts):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'GajanOpsHealth/1'}),timeout=timeout) as r:return {'healthy':200<=r.status<400,'attempts':n+1,'status':r.status}
  except (urllib.error.URLError,TimeoutError):
   if n+1<attempts:time.sleep(min(2**n,2))
 return {'healthy':False,'attempts':attempts,'status':'unreachable'}
def report(folder):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
 with connect() as c:
  accounts=[dict(x) for x in c.execute('SELECT * FROM accounts')];tasks=[dict(x) for x in c.execute('SELECT * FROM tasks')];events=[dict(x) for x in c.execute('SELECT * FROM events')]
 # Email and phone masked in distributable register; vault refs are references only.
 for a in accounts:
  a['vault_password_ref']='[REDACTED]' if a['vault_password_ref'] else None
  a['vault_backup_ref']='[REDACTED]' if a['vault_backup_ref'] else None
  if a['email']:a['email']='[REDACTED]'
  if a['phone']:a['phone']='[REDACTED]'
 for t in tasks: t['notes']='[REDACTED]' if t['notes'] else ''
 for e in events: e['detail']='[REDACTED]' if re.search(r'(?i)(password|secret|token|otp|backup.code)\s*[:=]',e['detail']) else e['detail']
 for name,data in [('account_register',accounts),('tasks',tasks),('run_log',events),('audit_report',audit())]:
  (folder/(name+'.json')).write_text(json.dumps(data,indent=2))
 return str(folder)
