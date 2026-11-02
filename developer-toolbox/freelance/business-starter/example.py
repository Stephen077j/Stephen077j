from core import quote, prepare_payment, notification, hash_password, verify_password, authorize
if __name__=="__main__":
    draft=quote([{"description":"Website design","quantity":1,"unit_price":"300000"}],currency="MGA")
    print("Quote:",draft)
    print("Payment request (NOT charged):",prepare_payment(draft,"DEMO_001"))
    print("Notification (NOT sent):",notification("email","example.invalid","Quote","Ready for review"))
    print("Access:",authorize("viewer","delete"))
    sample_hash=hash_password("fictional demo password")
    print("Password verification:",verify_password("fictional demo password",sample_hash))
