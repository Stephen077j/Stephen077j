"""DevCore API reference: SQLite, access controls, manual payment and email adapters.

Not production ready: no MFA, provider-specific charging, e-facture validation or SMS gateway.
"""
import hashlib
import json
import os
import re
import secrets
import time
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile, File
from pydantic import BaseModel, Field

from database import connect, initialize, audit
from security import check_password, digest_token, require_user, require_role
from services import calculate, now, smtp_send, money

app = FastAPI(title="DevCore Reference Business API", version="0.2.0")

@app.on_event("startup")
def startup():
    initialize()

class Login(BaseModel):
    username: str = Field(min_length=1,max_length=100)
    password: str

class Party(BaseModel):
    name: str = Field(min_length=1,max_length=200)
    address: str = Field(min_length=1,max_length=300)
    tax_id: str = Field(min_length=1,max_length=80)
    stat: str = Field(default="N/A",min_length=1,max_length=80)

class InvoiceRequest(BaseModel):
    seller: Party
    customer: Party
    due_at: str = Field(min_length=10,max_length=35)
    currency: str = Field(default="MGA",pattern="^[A-Z]{3}$")
    tax_percent: str = "0"
    lines: list[dict]

class PaymentRequest(BaseModel):
    invoice_id: int = Field(gt=0)
    reference: str = Field(min_length=3,max_length=64,pattern="^[A-Za-z0-9_-]+$")

class NotifyRequest(BaseModel):
    channel: str
    recipient: str = Field(min_length=1,max_length=254)
    subject: str = Field(min_length=1,max_length=200)
    body: str = Field(min_length=1,max_length=2000)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/auth/login")
def login(body:Login):
    with connect() as db:
        user=db.execute("SELECT * FROM users WHERE username=? AND active=1",(body.username,)).fetchone()
        if user is None or not check_password(body.password,user["password_hash"]):
            raise HTTPException(401,"Invalid credentials")
        token=secrets.token_urlsafe(32)
        expires=int(time.time())+3600
        db.execute("INSERT INTO sessions(token_hash,user_id,expires_at) VALUES(?,?,?)",
            (digest_token(token),user["id"],expires))
        audit(db,user["id"],"login",user["id"])
        return {"access_token":token,"token_type":"bearer","expires_in":3600}

@app.post("/auth/logout")
def logout(request:Request,user=Depends(require_user)):
    token=request.headers["authorization"].split(" ",1)[1]
    with connect() as db:
        db.execute("DELETE FROM sessions WHERE token_hash=?",(digest_token(token),))
        audit(db,user["id"],"logout",user["id"])
    return {"logged_out":True}

@app.get("/auth/me")
def me(user=Depends(require_user)):
    return user

@app.post("/invoices",status_code=201)
def issue_invoice(body:InvoiceRequest,user=Depends(require_role("admin","staff"))):
    # This demo does not generate legally valid Malagasy e-factures.
    try:
        totals=calculate(body.lines,body.tax_percent)
    except ValueError as exc: raise HTTPException(422,str(exc))
    if body.due_at[:10] < now()[:10]:
        raise HTTPException(422,"Due date cannot be in the past")
    with connect() as db:
        db.execute("BEGIN IMMEDIATE")
        # SQLite sequence allocated atomically. The illustrative number is not a certified fiscal number.
        cursor=db.execute("""INSERT INTO invoices(
           invoice_no,customer_name,customer_address,customer_tax_id,seller_name,seller_address,
           seller_tax_id,seller_stat,issued_at,due_at,currency,total,subtotal,tax,details_json,status
           ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'issued')""",
           ("PENDING-"+secrets.token_hex(8),body.customer.name,body.customer.address,body.customer.tax_id,
            body.seller.name,body.seller.address,body.seller.tax_id,body.seller.stat,
            now(),body.due_at,body.currency,totals["total"],totals["subtotal"],totals["tax"],
            json.dumps(totals["details"],ensure_ascii=False)))
        invoice_id=cursor.lastrowid
        invoice_no=f"DEMO-{invoice_id:08d}"
        db.execute("UPDATE invoices SET invoice_no=? WHERE id=?",(invoice_no,invoice_id))
        audit(db,user["id"],"invoice_issued",invoice_id)
        return {"id":invoice_id,"invoice_no":invoice_no,"status":"issued","currency":body.currency,**totals}

@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id:int,user=Depends(require_user)):
    with connect() as db:
        row=db.execute("SELECT * FROM invoices WHERE id=?",(invoice_id,)).fetchone()
        if row is None:raise HTTPException(404,"Invoice not found")
        result=dict(row)
        result["lines"]=json.loads(result.pop("details_json"))
        return result

@app.post("/payments",status_code=201)
def request_payment(body:PaymentRequest,user=Depends(require_role("admin","staff"))):
    with connect() as db:
        invoice=db.execute("SELECT * FROM invoices WHERE id=?",(body.invoice_id,)).fetchone()
        if invoice is None:raise HTTPException(404,"Invoice not found")
        if invoice["status"]!="issued":raise HTTPException(409,"Invoice not payable")
        try:
            db.execute("""INSERT INTO payments(invoice_id,reference,amount,currency,provider,status)
                        VALUES(?,?,?,?,?,?)""",
                (body.invoice_id,body.reference,invoice["total"],invoice["currency"],"manual","pending"))
        except Exception as exc:
            if isinstance(exc,__import__("sqlite3").IntegrityError):
                raise HTTPException(409,"Reference already exists") from exc
            raise
        audit(db,user["id"],"manual_payment_requested",body.reference)
    return {"reference":body.reference,"status":"pending","provider":"manual","paid":False}

@app.post("/payments/{reference}/confirm")
def confirm_payment(reference:str,user=Depends(require_role("admin"))):
    # Human confirmation only: this endpoint does not verify real bank settlement.
    with connect() as db:
        db.execute("BEGIN IMMEDIATE")
        result=db.execute("""UPDATE payments SET status='confirmed',confirmed_by=?,confirmed_at=?
            WHERE reference=? AND status='pending'""",(user["id"],now(),reference))
        if result.rowcount==0:raise HTTPException(409,"Missing payment or already processed")
        audit(db,user["id"],"manual_payment_confirmed",reference)
    return {"reference":reference,"status":"confirmed","verification":"human_only"}

@app.post("/notifications",status_code=201)
def enqueue(body:NotifyRequest,user=Depends(require_role("admin","staff"))):
    if body.channel not in ("email","sms","in_app"):raise HTTPException(422,"Unsupported channel")
    with connect() as db:
        cur=db.execute("""INSERT INTO notifications(channel,recipient,subject,body,status,created_at)
                     VALUES(?,?,?,?,?,?)""",(body.channel,body.recipient,body.subject,body.body,"queued",now()))
        audit(db,user["id"],"notification_queued",cur.lastrowid)
        return {"id":cur.lastrowid,"status":"queued","sent":False}

@app.post("/notifications/{notification_id}/send")
def send_notification(notification_id:int,user=Depends(require_role("admin"))):
    with connect() as db:
        row=db.execute("SELECT * FROM notifications WHERE id=?",(notification_id,)).fetchone()
        if row is None:raise HTTPException(404,"Notification not found")
        if row["status"]!="queued":raise HTTPException(409,"Notification already processed")
        if row["channel"]!="email":
            raise HTTPException(501,"SMS and in-app transport not configured")
        try:
            smtp_send(row["recipient"],row["subject"],row["body"])
        except Exception:
            db.execute("UPDATE notifications SET status='failed' WHERE id=?",(notification_id,))
            raise HTTPException(503,"SMTP delivery failed or not configured")
        db.execute("UPDATE notifications SET status='sent' WHERE id=?",(notification_id,))
        audit(db,user["id"],"smtp_sent",notification_id)
    return {"id":notification_id,"status":"sent"}

@app.post("/files",status_code=201)
async def upload(file:UploadFile=File(...),user=Depends(require_user)):
    if not file.filename or not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}",file.filename) or file.filename in (".",".."):
        raise HTTPException(422,"Invalid filename")
    data=await file.read(1024*1024+1)
    if len(data)>1024*1024:raise HTTPException(413,"File exceeds 1 MB")
    directory=Path(os.getenv("DEVCORE_PRIVATE_DIR","private_uploads")).resolve()
    directory.mkdir(parents=True,exist_ok=True,mode=0o700)
    key=secrets.token_hex(24)
    object_path=directory/key
    with object_path.open("xb") as target:target.write(data)
    object_path.chmod(0o600)
    with connect() as db:
        cur=db.execute("""INSERT INTO files(owner_id,filename,object_key,sha256,created_at)
                   VALUES(?,?,?,?,?)""",(user["id"],file.filename,key,hashlib.sha256(data).hexdigest(),now()))
        audit(db,user["id"],"file_uploaded",cur.lastrowid)
    return {"id":cur.lastrowid,"filename":file.filename,"sha256":hashlib.sha256(data).hexdigest()}

@app.get("/files/{file_id}")
def file_metadata(file_id:int,user=Depends(require_user)):
    with connect() as db:
        row=db.execute("SELECT id,owner_id,filename,sha256 FROM files WHERE id=?",(file_id,)).fetchone()
    if row is None or (row["owner_id"]!=user["id"] and user["role"]!="admin"):
        raise HTTPException(404,"File not found")
    return dict(row)
