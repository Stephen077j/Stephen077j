import json
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"catalog.json"
class CatalogTests(unittest.TestCase):
 def test_shape(self):
  data=json.loads(p.read_text(encoding="utf-8"))
  self.assertEqual(data["count"],len(data["entries"]))
  self.assertGreaterEqual(len(data["entries"]),12)
 def test_existing_not_called_forks(self):
  data=json.loads(p.read_text(encoding="utf-8"))
  self.assertTrue(all("not verified fork" in e["status"] for e in data["entries"] if "Stephen077j/" in e["url"]))
 def test_sectors(self):
  data=json.loads(p.read_text(encoding="utf-8"))
  self.assertTrue({"bible-hymns","education","police-public-safety","health","commerce"}.issubset({e["sector"] for e in data["entries"]}))
 def test_urls_unique(self):
  entries=json.loads(p.read_text(encoding="utf-8"))["entries"]
  self.assertEqual(len(entries),len(set(e["url"] for e in entries)))
