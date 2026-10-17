import os,tempfile,unittest
from app import core as c
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();c.DB=self.tmp.name+'/test.db';c.init()
 def tearDown(self):self.tmp.cleanup()
 def test_idempotent(self):
  a=c.register('Example','ops');b=c.register('Example','ops');self.assertEqual(a['id'],b['id'])
 def test_bio(self):
  a=c.register('Example','ops');self.assertRaises(ValueError,c.update,a['id'],bio='x'*151)
 def test_secret_ref(self):
  a=c.register('Example','ops');self.assertRaises(ValueError,c.update,a['id'],vault_password_ref='plaintext')
 def test_resume(self):
  a=c.register('Example','ops');t=c.task(a['id'],'signup','ops');c.complete(t['id']);self.assertEqual(c.task(a['id'],'signup','ops')['status'],'done')
 def test_audit(self):
  a=c.register('Example','ops');self.assertTrue(c.audit());self.assertTrue(c.audit())
if __name__=='__main__':unittest.main()
