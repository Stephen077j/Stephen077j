import tempfile
import unittest
from pathlib import Path
from core import authorize,hash_password,verify_password,quote,prepare_payment,notification,save_private

class BusinessStarterTests(unittest.TestCase):
 def test_quote(self):
  q=quote([{"description":"Service","quantity":2,"unit_price":"12.25"}],"10")
  self.assertEqual(q["total"],"26.95")
  self.assertEqual(q["tax"],"2.45")
 def test_bad_quantity(self):
  with self.assertRaises(ValueError):quote([{"description":"X","quantity":True,"unit_price":"1"}])
 def test_bad_amount(self):
  with self.assertRaises(ValueError):quote([{"description":"X","quantity":1,"unit_price":"NaN"}])
 def test_password_hash(self):
  value=hash_password("strong test passphrase")
  self.assertTrue(verify_password("strong test passphrase",value))
  self.assertFalse(verify_password("wrong password",value))
 def test_permissions(self):
  self.assertTrue(authorize("admin","delete"))
  self.assertFalse(authorize("viewer","delete"))
 def test_payment_not_charged(self):
  q=quote([{"description":"S","quantity":1,"unit_price":"20"}])
  self.assertEqual(prepare_payment(q,"INV_2026_001")["status"],"pending_manual_confirmation")
 def test_notification_not_sent(self):
  self.assertEqual(notification("sms","test-recipient","Reminder","Hi")["status"],"queued_not_sent")
 def test_private_store_and_no_overwrite(self):
  with tempfile.TemporaryDirectory() as d:
   self.assertEqual(save_private(d,"account1","sample.txt",b"hello")["size"],5)
   self.assertEqual((Path(d)/"account1"/"sample.txt").read_bytes(),b"hello")
   with self.assertRaises(FileExistsError):save_private(d,"account1","sample.txt",b"again")
 def test_traversal_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):save_private(d,"account1","../private",b"x")
