import unittest
from main import format_time
class TimeTests(unittest.TestCase):
    def test_format(self):
        self.assertEqual(format_time(65),"01:05")
    def test_negative(self):
        with self.assertRaises(ValueError):format_time(-1)
