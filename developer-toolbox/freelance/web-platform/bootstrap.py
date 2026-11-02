"""Create a first local administrator from environment variables; not for public self-registration."""
import os
from database import initialize, connect
from security import password_hash

def main():
    username=os.getenv("DEVCORE_ADMIN_USER","").strip()
    password=os.getenv("DEVCORE_ADMIN_PASSWORD","")
    if not username or not password:
        raise SystemExit("Set DEVCORE_ADMIN_USER and DEVCORE_ADMIN_PASSWORD (12+ characters)")
    initialize()
    with connect() as db:
        db.execute("INSERT INTO users(username,password_hash,role) VALUES (?,?,?)",
            (username,password_hash(password),"admin"))
    print("Admin created; remove the bootstrap password from your environment after use.")

if __name__=="__main__":
    main()
