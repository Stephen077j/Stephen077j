import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from search import search

class FreelanceCatalogTests(unittest.TestCase):
    def test_eighteen_categories(self):
        self.assertEqual(len(search()),18)
    def test_payments(self):
        self.assertTrue(any(x["id"]=="05-payments" for x in search("payment")))
    def test_specific_category(self):
        self.assertEqual(len(search(category="14-hosting")),1)
    def test_case_insensitive(self):
        self.assertEqual(search("AUTH"),search("auth"))
    def test_unknown(self):
        self.assertEqual(search("missing_keyword_000"),[])
