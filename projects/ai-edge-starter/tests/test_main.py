import tempfile
import unittest
from pathlib import Path
from main import model_manifest
class Tests(unittest.TestCase):
 def test_hash(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"demo.onnx";p.write_bytes(b"demo")
   self.assertEqual(len(model_manifest(p)["sha256"]),64)
 def test_extension(self):
  with self.assertRaises(ValueError):model_manifest("not-model.exe")
