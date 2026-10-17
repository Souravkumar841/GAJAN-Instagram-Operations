import unittest
from pathlib import Path
class WebAssetsTest(unittest.TestCase):
 def test_assets_exist(self):
  root=Path(__file__).resolve().parents[1]
  self.assertTrue((root/'web/index.html').exists())
  self.assertTrue((root/'web/app.js').exists())
 def test_import(self):
  from app.web import Handler
  self.assertTrue(Handler)
