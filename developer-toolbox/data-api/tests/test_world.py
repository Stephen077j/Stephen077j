import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from search_world import search, REGISTRY

class WorldRegistryTests(unittest.TestCase):
    def test_registry_has_sources(self):
        self.assertGreaterEqual(len(search()), 50)
    def test_categories(self):
        self.assertTrue(any(x["name"]=="Open-Meteo" for x in search(category="weather-earth")))
    def test_madagascar(self):
        self.assertTrue(any("Madagascar" in x["name"] for x in search("madagascar")))
    def test_search_casefold(self):
        self.assertEqual(search("weaTher"), search("WEATHER"))
    def test_urls_and_unique_names(self):
        results=search()
        self.assertEqual(len({x["name"] for x in results}),len(results))
        self.assertTrue(all(x["documentation"].startswith("https://") for x in results))
    def test_no_false_access_guarantees(self):
        self.assertTrue(all("reference only" in x["review_status"] for x in search()))
