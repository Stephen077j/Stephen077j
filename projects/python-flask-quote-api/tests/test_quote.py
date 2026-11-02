import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quote import calculate_quote


class QuoteCalculationTests(unittest.TestCase):
    def test_totals(self):
        result = calculate_quote({
            "items": [{"description": "Maintenance", "quantity": 2, "unit_price": "19.95"}],
            "tax_percent": 10,
        })
        self.assertEqual(result["subtotal"], "39.90")
        self.assertEqual(result["tax"], "3.99")
        self.assertEqual(result["total"], "43.89")

    def test_round_half_up(self):
        result = calculate_quote({"items": [
            {"description": "Example", "quantity": 1, "unit_price": "0.005"}]})
        self.assertEqual(result["total"], "0.01")

    def test_reject_invalid_quantity(self):
        for quantity in (0, -1, True, 1.5, 10001):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError):
                    calculate_quote({"items": [
                        {"description": "Item", "quantity": quantity, "unit_price": 2}]})

    def test_reject_invalid_amounts(self):
        for price in ("nan", "Infinity", -1, None):
            with self.subTest(price=price):
                with self.assertRaises(ValueError):
                    calculate_quote({"items": [
                        {"description": "Item", "quantity": 1, "unit_price": price}]})


if __name__ == "__main__":
    unittest.main()
