import json
import tempfile
import unittest
from pathlib import Path
from integrity import digest, inventory, verify


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "nested").mkdir()
        (self.root / "nested" / "école.txt").write_text("Bonjour Madagascar", encoding="utf-8")

    def data(self):
        return inventory(self.root, self.root / "manifest.json")

    def test_inventory_and_verify(self):
        self.assertEqual(self.data()["files"][0]["path"], "nested/école.txt")
        self.assertTrue(verify(self.root, self.data())["valid"])

    def test_change_same_size_detected(self):
        data = self.data()
        (self.root / "nested" / "école.txt").write_text("Bonjour MadagascaR", encoding="utf-8")
        self.assertEqual(verify(self.root, data)["errors"][0]["code"], "hash_mismatch")

    def test_missing_file(self):
        data = self.data()
        (self.root / "nested" / "école.txt").unlink()
        self.assertEqual(verify(self.root, data)["errors"][0]["code"], "missing")

    def test_size_change(self):
        data = self.data()
        (self.root / "nested" / "école.txt").write_text("x", encoding="utf-8")
        self.assertEqual(verify(self.root, data)["errors"][0]["code"], "size_mismatch")

    def test_reject_traversal(self):
        data = self.data()
        data["files"][0]["path"] = "../secret.txt"
        with self.assertRaises(ValueError):
            verify(self.root, data)

    def test_reject_duplicate(self):
        data = self.data()
        data["files"].append(dict(data["files"][0]))
        with self.assertRaises(ValueError):
            verify(self.root, data)

    def test_manifest_excluded(self):
        (self.root / "manifest.json").write_text("{}")
        self.assertEqual(len(self.data()["files"]), 1)

    def test_symlink_not_followed(self):
        (self.root / "link.txt").symlink_to(self.root / "nested" / "école.txt")
        self.assertEqual(len(self.data()["files"]), 1)

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            verify(self.root, {"files": []})

    def test_sha256_known_value(self):
        (self.root / "empty").write_bytes(b"")
        self.assertEqual(digest(self.root / "empty"),
                         "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

    def test_json_roundtrip(self):
        self.assertTrue(verify(self.root, json.loads(json.dumps(self.data())))["valid"])


if __name__ == "__main__":
    unittest.main()
