import csv
import tempfile
import unittest
from pathlib import Path
from sentiment import classify, process_csv


class SentimentTests(unittest.TestCase):
    def test_multilingual(self):
        for text in ('Très bon', 'good', 'tsara'):
            self.assertEqual(classify(text)[0], 'positive')
        for text in ('mauvais', 'bad', 'ratsy'):
            self.assertEqual(classify(text)[0], 'negative')

    def test_negation(self):
        self.assertEqual(classify('pas bon')[0], 'negative')
        self.assertEqual(classify('not bad')[0], 'positive')
        self.assertEqual(classify('tsy tsara')[0], 'negative')

    def test_neutral(self):
        self.assertEqual(classify('livraison demain'), ('neutral', 0))

    def test_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            src, dst = Path(folder) / 'in.csv', Path(folder) / 'out.csv'
            src.write_text('id,comment\n1,tsara\n2,pas bon\n', encoding='utf-8')
            self.assertEqual(process_csv(src, dst), 2)
            with dst.open(encoding='utf-8', newline='') as f:
                rows = list(csv.DictReader(f))
            self.assertEqual([r['sentiment'] for r in rows], ['positive', 'negative'])
            with self.assertRaises(ValueError):
                process_csv(src, src)

    def test_missing_column(self):
        with tempfile.TemporaryDirectory() as folder:
            src, dst = Path(folder) / 'in.csv', Path(folder) / 'out.csv'
            src.write_text('other\nhello\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                process_csv(src, dst)


if __name__ == '__main__':
    unittest.main()
