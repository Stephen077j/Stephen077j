import csv
import tempfile
import unittest
from pathlib import Path
from guard import validate

class GuardTests(unittest.TestCase):
    def check(self, content, required, unique=None):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.csv"
            path.write_text(content, encoding="utf-8-sig")
            return validate(path, required, unique)

    def test_valid_multilingual_csv(self):
        result = self.check("id,anarana,ville\n1,Soa,Fianarantsoa\n2,Jean,Antsirabe\n", ["id", "anarana"], ["id"])
        self.assertTrue(result["valid"])
        self.assertEqual(result["rows"], 2)

    def test_missing_column(self):
        result = self.check("id,name\n1,Soa\n", ["email"])
        self.assertEqual(result["errors"][0]["code"], "missing_column")

    def test_duplicate_id(self):
        result = self.check("id,name\n1,A\n1,B\n", ["id"], ["id"])
        self.assertIn("duplicate_value", [e["code"] for e in result["errors"]])

    def test_empty_required(self):
        result = self.check("id,name\n1, \n", ["name"])
        self.assertIn("empty_required", [e["code"] for e in result["errors"]])

    def test_malformed_row(self):
        result = self.check("id,name\n1,A,extra\n", ["id"])
        self.assertIn("column_count", [e["code"] for e in result["errors"]])

    def test_duplicate_header(self):
        result = self.check("id,id\n1,2\n", ["id"])
        self.assertIn("duplicate_header", [e["code"] for e in result["errors"]])

    def test_empty_file(self):
        result = self.check("", ["id"])
        self.assertFalse(result["valid"])

    def test_no_sensitive_values_in_report(self):
        result = self.check("id,name\n1,SECRETNAME\n1,OTHER\n", ["id"], ["id"])
        self.assertNotIn("SECRETNAME", str(result))
        self.assertNotIn("OTHER", str(result))

    def test_schema_rejects_duplicate_column_spec(self):
        with self.assertRaises(ValueError):
            self.check("id\n1\n", ["id", "id"])

if __name__ == "__main__":
    unittest.main()
