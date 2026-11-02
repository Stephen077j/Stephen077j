import os
import tempfile
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

from database import initialize, connect
from security import password_hash
from app import app

class APITests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        os.environ["DEVCORE_DB"]=str(Path(self.tmp.name)/"test.db")
        os.environ["DEVCORE_PRIVATE_DIR"]=str(Path(self.tmp.name)/"objects")
        initialize()
        with connect() as db:
            db.execute("INSERT INTO users(username,password_hash,role) VALUES(?,?,?)",
                       ("admin",password_hash("correct horse battery staple"),"admin"))
            db.execute("INSERT INTO users(username,password_hash,role) VALUES(?,?,?)",
                       ("reader",password_hash("correct horse battery staple"),"viewer"))
        self.client=TestClient(app)
        self.admin=self.login("admin")
        self.reader=self.login("reader")
    def tearDown(self):
        self.tmp.cleanup()
        os.environ.pop("DEVCORE_DB",None)
        os.environ.pop("DEVCORE_PRIVATE_DIR",None)
    def login(self,name):
        r=self.client.post("/auth/login",json={"username":name,"password":"correct horse battery staple"})
        self.assertEqual(r.status_code,200,r.text)
        return {"Authorization":"Bearer "+r.json()["access_token"]}
    def invoice(self):
        return {"seller":{"name":"Test Vendor","address":"Sample address","tax_id":"TEST-NIF","stat":"TEST-STAT"},
                "customer":{"name":"Test Buyer","address":"Sample address","tax_id":"TEST-NIF"},
                "due_at":"2099-01-01","lines":[{"description":"Service","quantity":2,"unit_price":"12.25"}],
                "tax_percent":"10","currency":"MGA"}
    def test_authentication(self):
        self.assertEqual(self.client.get("/auth/me").status_code,401)
        self.assertEqual(self.client.post("/auth/login",json={"username":"admin","password":"wrong"}).status_code,401)
        self.assertEqual(self.client.get("/auth/me",headers=self.reader).json()["role"],"viewer")
        self.assertTrue(self.client.post("/auth/logout",headers=self.reader).json()["logged_out"])
        self.assertEqual(self.client.get("/auth/me",headers=self.reader).status_code,401)
    def test_invoices_and_permissions(self):
        self.assertEqual(self.client.post("/invoices",json=self.invoice(),headers=self.reader).status_code,403)
        r=self.client.post("/invoices",json=self.invoice(),headers=self.admin)
        self.assertEqual(r.status_code,201,r.text)
        self.assertEqual(r.json()["total"],"26.95")
        self.assertEqual(self.client.get("/invoices/1",headers=self.reader).status_code,200)
    def test_payment_confirm_once(self):
        self.client.post("/invoices",json=self.invoice(),headers=self.admin)
        r=self.client.post("/payments",json={"invoice_id":1,"reference":"DEMO_001"},headers=self.admin)
        self.assertEqual(r.status_code,201,r.text)
        self.assertFalse(r.json()["paid"])
        self.assertEqual(self.client.post("/payments/DEMO_001/confirm",headers=self.reader).status_code,403)
        self.assertEqual(self.client.post("/payments/DEMO_001/confirm",headers=self.admin).status_code,200)
        self.assertEqual(self.client.post("/payments/DEMO_001/confirm",headers=self.admin).status_code,409)
    def test_notification_never_claims_sent(self):
        r=self.client.post("/notifications",json={"channel":"sms","recipient":"fictional","subject":"Hello","body":"Test"},headers=self.admin)
        self.assertEqual(r.status_code,201)
        self.assertFalse(r.json()["sent"])
        self.assertEqual(self.client.post(f"/notifications/{r.json()['id']}/send",headers=self.admin).status_code,501)
    def test_private_file_access(self):
        r=self.client.post("/files",headers=self.admin,files={"file":("demo.txt",b"private","text/plain")})
        self.assertEqual(r.status_code,201,r.text)
        ident=r.json()["id"]
        self.assertEqual(self.client.get(f"/files/{ident}",headers=self.reader).status_code,404)
        self.assertEqual(self.client.get(f"/files/{ident}",headers=self.admin).status_code,200)
    def test_path_traversal(self):
        r=self.client.post("/files",headers=self.admin,files={"file":("../secret",b"x","application/octet-stream")})
        self.assertEqual(r.status_code,422)
if __name__=="__main__":unittest.main()
