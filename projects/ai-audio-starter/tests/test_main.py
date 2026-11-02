import tempfile
import wave
import unittest
from pathlib import Path
from main import describe_wav
class Tests(unittest.TestCase):
 def test_wav(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"test.wav"
   with wave.open(str(p),"wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(8000);w.writeframes(b"\x00\x00"*8000)
   self.assertEqual(describe_wav(p)["duration_seconds"],1.0)
