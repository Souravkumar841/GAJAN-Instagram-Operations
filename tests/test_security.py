import tempfile,unittest
from app import core as c
class SecurityTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();c.DB=self.tmp.name+'/test.db';c.init()
 def tearDown(self):self.tmp.cleanup()
 def test_no_secrets_in_notes(self):
  a=c.register('Example','ops');t=c.task(a['id'],'verify','ops')
  with self.assertRaises(ValueError):c.complete(t['id'],'password=example123')
 def test_no_unverified_verified_status(self):
  a=c.register('Example','ops')
  with self.assertRaises(ValueError):c.update(a['id'],status='verified')
 def test_reports_redact_notes_and_vault_refs(self):
  a=c.register('Example','ops');t=c.task(a['id'],'verify','ops');c.complete(t['id'],'private customer detail')
  c.update(a['id'],vault_password_ref='vault://safe/reference')
  c.report(self.tmp.name+'/reports')
  from pathlib import Path
  self.assertNotIn('private customer detail',(Path(self.tmp.name)/'reports/tasks.json').read_text())
  self.assertNotIn('vault://safe/reference',(Path(self.tmp.name)/'reports/account_register.json').read_text())
