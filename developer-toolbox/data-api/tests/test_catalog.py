import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from validate import load_catalog

class CatalogTests(unittest.TestCase):
    def test_catalog_valid(self):
        data=load_catalog()
        self.assertGreaterEqual(len(data["sources"]),15)
    def test_madagascar_included(self):
        data=load_catalog()
        self.assertTrue(any(x["category"]=="madagascar" for x in data["sources"]))
    def test_api_directory_included(self):
        data=load_catalog()
        self.assertTrue(any(x["category"]=="api-directory" for x in data["sources"]))
