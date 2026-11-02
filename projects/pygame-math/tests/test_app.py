import random
import unittest
from main import make_question
class MathTests(unittest.TestCase):
    def test_question(self):
        a,b,answer=make_question(random.Random(1))
        self.assertEqual(a+b,answer)
        self.assertTrue(1<=a<=12 and 1<=b<=12)
