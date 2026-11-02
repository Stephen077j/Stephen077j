import unittest
from main import evaluate
class Tests(unittest.TestCase):
 def test_pass(self):
  self.assertTrue(evaluate({"f1":0.9},{"f1":0.8})["pass"])
 def test_fail(self):
  self.assertFalse(evaluate({"f1":0.4},{"f1":0.8})["pass"])
 def test_missing(self):
  with self.assertRaises(ValueError):evaluate({},{"f1":0.8})
