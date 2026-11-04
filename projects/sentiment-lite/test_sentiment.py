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


    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            src, dst = Path(folder) / 'in.csv', Path(folder) / 'out.csv'
            src.write_text('id,comment\\n1,good\\n', encoding='utf-8')
            dst.write_text('IMPORTANT ORIGINAL CONTENT\\n', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                process_csv(src, dst)
            self.assertEqual(dst.read_text(encoding='utf-8'), 'IMPORTANT ORIGINAL CONTENT\\n')

    def test_no_output_created_for_missing_column(self):
        with tempfile.TemporaryDirectory() as folder:
            src, dst = Path(folder) / 'in.csv', Path(folder) / 'out.csv'
            src.write_text('other\\nhello\\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                process_csv(src, dst)
            self.assertFalse(dst.exists())

    def test_bom_input_preserves_original_columns(self):
        with tempfile.TemporaryDirectory() as folder:
            src, dst = Path(folder) / 'in.csv', Path(folder) / 'out.csv'
            src.write_text('id,comment,source\\n1,tsara,MG\\n', encoding='utf-8-sig')
            self.assertEqual(process_csv(src, dst), 1)
            with dst.open(encoding='utf-8', newline='') as inp:
                rows = list(csv.DictReader(inp))
            self.assertEqual(rows[0]['id'], '1')
            self.assertEqual(rows[0]['source'], 'MG')
            self.assertEqual(rows[0]['sentiment'], 'positive')

if __name__ == '__main__':
    unittest.main()
