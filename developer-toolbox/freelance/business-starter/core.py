"""Dependency-free reusable business primitives; demo only, not a production identity/payment system."""
import hashlib
import hmac
import json
import os
import re
import secrets
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

CENTS=Decimal("0.01")
def money(value):
    if isinstance(value,bool): raise ValueError("invalid amount")
    try: amount=Decimal(str(value))
    except (InvalidOperation,TypeError): raise ValueError("invalid amount") from None
    if not amount.is_finite() or amount < 0 or amount > 1000000000: raise ValueError("amount outside supported range")
    return amount.quantize(CENTS,rounding=ROUND_HALF_UP)

def quote(lines,tax_percent="0",currency="MGA"):
    if not isinstance(lines,list) or not 1<=len(lines)<=100: raise ValueError("1-100 lines required")
    if not isinstance(currency,str) or not re.fullmatch(r"[A-Z]{3}",currency): raise ValueError("ISO currency code required")
    rate=Decimal(str(tax_percent))
    if not rate.is_finite() or not 0<=rate<=100: raise ValueError("invalid tax percentage")
    detailed=[]
    subtotal=Decimal("0")
    for item in lines:
        if not isinstance(item,dict) or not isinstance(item.get("description"),str) or not 1<=len(item["description"].strip())<=200: raise ValueError("invalid description")
        qty=item.get("quantity")
        if isinstance(qty,bool) or not isinstance(qty,int) or not 1<=qty<=10000: raise ValueError("invalid quantity")
        unit=money(item.get("unit_price"))
        total=(unit*qty).quantize(CENTS,rounding=ROUND_HALF_UP)
        subtotal+=total
        detailed.append({"description":item["description"].strip(),"quantity":qty,"unit_price":str(unit),"total":str(total)})
    tax=(subtotal*rate/100).quantize(CENTS,rounding=ROUND_HALF_UP)
    return {"currency":currency,"lines":detailed,"subtotal":str(subtotal),"tax":str(tax),"total":str(subtotal+tax),"status":"draft"}

def hash_password(password,rounds=250000):
    if not isinstance(password,str) or len(password)<12 or len(password)>1024: raise ValueError("password length must be 12-1024")
    salt=secrets.token_bytes(16)
    derived=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,rounds)
    return f"pbkdf2_sha256${rounds}${salt.hex()}${derived.hex()}"

def verify_password(password,stored):
    try:
        algorithm,rounds_text,salt_hex,hash_hex=stored.split("$")
        if algorithm!="pbkdf2_sha256":return False
        rounds=int(rounds_text)
        if not 100000<=rounds<=1000000:return False
        expected=bytes.fromhex(hash_hex)
        actual=hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt_hex),rounds)
        return hmac.compare_digest(actual,expected)
    except (AttributeError,ValueError,TypeError):return False

def authorize(role,action):
    policy={"admin":{"read","write","delete"},"staff":{"read","write"},"viewer":{"read"}}
    return action in policy.get(role,set())

def prepare_payment(quote_data,reference):
    if not isinstance(reference,str) or not re.fullmatch(r"[A-Za-z0-9_-]{3,64}",reference):raise ValueError("invalid reference")
    if not isinstance(quote_data,dict) or quote_data.get("status")!="draft":raise ValueError("invalid quotation")
    return {"reference":reference,"amount":quote_data["total"],"currency":quote_data["currency"],"status":"pending_manual_confirmation","provider":"none"}

def notification(kind,recipient,subject,body):
    if kind not in ("email","sms","in_app"):raise ValueError("unknown channel")
    if not all(isinstance(x,str) and 1<=len(x)<=2000 for x in (recipient,subject,body)):raise ValueError("invalid message")
    return {"channel":kind,"recipient":recipient,"subject":subject,"body":body,"status":"queued_not_sent"}

def save_private(root,owner,filename,data):
    if not isinstance(owner,str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,40}",owner):raise ValueError("invalid owner")
    if not isinstance(filename,str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}",filename) or filename in (".",".."):raise ValueError("invalid filename")
    if not isinstance(data,bytes) or len(data)>1024*1024:raise ValueError("file must be bytes <= 1MB")
    base=Path(root).resolve()
    target=base/owner
    target.mkdir(parents=True,exist_ok=True,mode=0o700)
    path=target/filename
    if path.is_symlink() or path.exists():raise FileExistsError("file already exists")
    with path.open("xb") as output:output.write(data)
    path.chmod(0o600)
    return {"owner":owner,"filename":filename,"sha256":hashlib.sha256(data).hexdigest(),"size":len(data)}
