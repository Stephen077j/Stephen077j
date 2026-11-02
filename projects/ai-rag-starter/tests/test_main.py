import unittest
from main import retrieve
class Tests(unittest.TestCase):
 def test_retrieval(self):
  self.assertEqual(retrieve("school fee",[{"id":"a","text":"school fee rules"},{"id":"b","text":"weather"}])[0]["source"],"a")
 def test_no_evidence(self):
  self.assertEqual(retrieve("zzz",[{"id":"a","text":"weather"}]),[])
 def test_invalid(self):
  with self.assertRaises(ValueError):retrieve("",[])
