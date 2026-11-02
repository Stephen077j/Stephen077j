"""Minimal security components for a tutorial. No MFA, refresh tokens, lockout or SSO."""
import hashlib
import hmac
import secrets
import time
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database import connect

bearer = HTTPBearer(auto_error=False)

def password_hash(password):
    if not isinstance(password,str) or not 12 <= len(password) <= 1024:
        raise ValueError("Password must be 12-1024 characters")
    salt = secrets.token_bytes(16)
    iterations = 350000
    value = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2${iterations}${salt.hex()}${value.hex()}"

def check_password(password, encoded):
    try:
        algorithm, iteration, salt, stored = encoded.split("$")
        if algorithm != "pbkdf2": return False
        rounds = int(iteration)
        if not 100000 <= rounds <= 1000000: return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), rounds)
        return hmac.compare_digest(actual, bytes.fromhex(stored))
    except (ValueError, TypeError, AttributeError): return False

def digest_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

def require_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(401,"Bearer token required")
    with connect() as db:
        row = db.execute("""SELECT u.id,u.username,u.role FROM sessions s JOIN users u ON u.id=s.user_id
            WHERE s.token_hash=? AND s.expires_at>? AND u.active=1""",
            (digest_token(credentials.credentials), int(time.time()))).fetchone()
    if row is None: raise HTTPException(401,"Invalid or expired token")
    return dict(row)

def require_role(*roles):
    def dependency(user=Depends(require_user)):
        if user["role"] not in roles: raise HTTPException(403,"Insufficient role")
        return user
    return dependency
