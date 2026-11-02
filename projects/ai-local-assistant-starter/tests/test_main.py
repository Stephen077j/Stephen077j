import unittest
from main import ask
class Tests(unittest.TestCase):
 def test_mock(self):
  self.assertEqual(ask("Hello",transport=lambda request:{"response":"Hi"}),"Hi")
 def test_remote_rejected(self):
  with self.assertRaises(ValueError):ask("Hello",base_url="https://external.example")
