import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from search import search

class RegistryTests(unittest.TestCase):
    def test_reference_count(self):
        self.assertGreaterEqual(len(search()),60)
    def test_categories(self):
        self.assertGreaterEqual(len({x["category"] for x in search()}),9)
    def test_json_schema(self):
        self.assertTrue(any(x["name"]=="JSON Schema" for x in search("schema")))
    def test_mock_server(self):
        self.assertTrue(any(x["name"]=="WireMock" for x in search("mock")))
    def test_unique_repos(self):
        items=search()
        self.assertEqual(len(items),len({x["url"] for x in items}))
    def test_case_insensitive(self):
        self.assertEqual(search("GRAPHQL"),search("graphql"))
