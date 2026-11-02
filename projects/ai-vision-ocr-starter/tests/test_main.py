import tempfile
import unittest
from pathlib import Path
from main import threshold_pgm
class Tests(unittest.TestCase):
 def test_binary(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"image.pgm"
   p.write_text("P2\n2 2\n255\n0 255\n200 20\n")
   self.assertEqual(threshold_pgm(p),[[1,0],[0,1]])
