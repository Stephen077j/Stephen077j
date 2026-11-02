import unittest
from main import summarize
class DashboardTests(unittest.TestCase):
    def test_summary(self):
        self.assertEqual(summarize("amount\n10\n20\n"),{"count":2,"total":30.0,"average":15.0})
    def test_empty(self):
        self.assertEqual(summarize("amount\n")["count"],0)
