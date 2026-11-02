import unittest
from classifier import train, predict, tokenize

EXAMPLES=[
    ("hello need help", "support"),
    ("please help", "support"),
    ("track my delivery", "orders"),
    ("my package arrived", "orders"),
    ("quote and price", "sales"),
    ("product price", "sales"),
]


class ClassifierTests(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(tokenize("HELLO, World!"), ["hello", "world"])

    def test_reject_empty(self):
        with self.assertRaises(ValueError):
            train([])

    def test_classifier_returns_known_label(self):
        model=train(EXAMPLES)
        result=predict(model, "track package")
        self.assertIn(result["label"], model["labels"])
        self.assertEqual(set(result["scores"]), set(model["labels"]))

    def test_probabilities(self):
        result=predict(train(EXAMPLES),"help")
        self.assertAlmostEqual(sum(result["scores"].values()),1.0,places=4)

    def test_empty_input_remains_valid(self):
        result=predict(train(EXAMPLES),"")
        self.assertIn(result["label"], ["orders","sales","support"])


if __name__=="__main__":
    unittest.main()
