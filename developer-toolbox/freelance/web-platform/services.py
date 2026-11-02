"""Safe calculation and notification adapters with no false delivery confirmations."""
import hashlib
import hmac
import json
import os
import smtplib
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from email.message import EmailMessage

def money(value):
    try: number=Decimal(str(value))
    except (InvalidOperation,TypeError,ValueError): raise ValueError("Invalid amount") from None
    if not number.is_finite() or number < 0 or number > 100000000: raise ValueError("Invalid amount")
    return number.quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)

def calculate(lines, tax_percent):
    if not isinstance(lines,list) or not 1<=len(lines)<=100: raise ValueError("1-100 invoice lines required")
    tax_rate=Decimal(str(tax_percent))
    if not tax_rate.is_finite() or not 0<=tax_rate<=100: raise ValueError("Invalid tax percentage")
    subtotal=Decimal("0.00")
    details=[]
    for line in lines:
        if not isinstance(line,dict) or not isinstance(line.get("description"),str) or not line["description"].strip():
            raise ValueError("Missing description")
        qty=line.get("quantity")
        if not isinstance(qty,int) or isinstance(qty,bool) or not 1<=qty<=10000: raise ValueError("Invalid quantity")
        unit=money(line.get("unit_price"))
        total=(unit*qty).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
        details.append({"description":line["description"].strip()[:200],"quantity":qty,"unit_price":str(unit),"total":str(total)})
        subtotal+=total
    tax=(subtotal*tax_rate/100).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
    return {"details":details,"subtotal":str(subtotal),"tax":str(tax),"total":str(subtotal+tax)}

def smtp_send(recipient,subject,body):
    """Send only when fully configured; errors propagate, never mark sent on failure."""
    host=os.getenv("SMTP_HOST")
    user=os.getenv("SMTP_USERNAME")
    password=os.getenv("SMTP_PASSWORD")
    sender=os.getenv("SMTP_FROM")
    port=int(os.getenv("SMTP_PORT","587"))
    if not (host and user and password and sender):
        raise RuntimeError("SMTP delivery not configured")
    message=EmailMessage()
    message["From"]=sender; message["To"]=recipient; message["Subject"]=subject
    message.set_content(body)
    with smtplib.SMTP(host,port,timeout=15) as connection:
        connection.starttls()
        connection.login(user,password)
        connection.send_message(message)

def verify_webhook(raw_body, signature, secret):
    if not secret: raise ValueError("Webhook secret not configured")
    digest=hmac.new(secret.encode(),raw_body,hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest,signature or "")

def now():
    return datetime.now(timezone.utc).isoformat()
