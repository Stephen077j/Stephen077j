import unittest
from main import retrieve
class Tests(unittest.TestCase):
 def test_retrieval(self):
  self.assertEqual(retrieve("school fee",[{"id":"a","text":"school fee rules"},{"id":"b","text":"weather"}])[0]["source"],"a")
 def test_no_evidence(self):
  self.assertEqual(retrieve("zzz",[{"id":"a","text":"weather"}]),[])
 def test_invalid(self):
  with self.assertRaises(ValueError):retrieve("",[])

 def test_frequency_ranking(self):
  docs=[{"id":"low","text":"school event"},{"id":"high","text":"school school school event"}]
  self.assertEqual(retrieve("school",docs)[0]["source"],"high")
 def test_duplicate_id(self):
  with self.assertRaises(ValueError):
   retrieve("school",[{"id":"a","text":"school"},{"id":"a","text":"school"}])
 def test_limit_rejected(self):
  with self.assertRaises(ValueError):retrieve("school",[],True)
 def test_deterministic_tiebreaker(self):
  docs=[{"id":"z","text":"school"},{"id":"a","text":"school"}]
  self.assertEqual(retrieve("school",docs)[0]["source"],"a")
