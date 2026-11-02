"""SQLite data access; demo schema, not a production migration framework."""
import os
import sqlite3
from pathlib import Path

def connect():
    path = Path(os.getenv("DEVCORE_DB", "devcore_demo.sqlite3"))
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(path), timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA busy_timeout=5000")
    return db

def initialize():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT NOT NULL UNIQUE,
          password_hash TEXT NOT NULL,
          role TEXT NOT NULL CHECK(role IN ('admin','staff','viewer')),
          active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS sessions (
          token_hash TEXT PRIMARY KEY,
          user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          expires_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS invoices (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          invoice_no TEXT NOT NULL UNIQUE,
          customer_name TEXT NOT NULL,
          customer_address TEXT NOT NULL,
          customer_tax_id TEXT NOT NULL,
          seller_name TEXT NOT NULL,
          seller_address TEXT NOT NULL,
          seller_tax_id TEXT NOT NULL,
          seller_stat TEXT NOT NULL,
          issued_at TEXT NOT NULL,
          due_at TEXT NOT NULL,
          currency TEXT NOT NULL,
          total TEXT NOT NULL,
          subtotal TEXT NOT NULL,
          tax TEXT NOT NULL,
          details_json TEXT NOT NULL,
          status TEXT NOT NULL CHECK(status IN ('issued','cancelled'))
        );
        CREATE TABLE IF NOT EXISTS payments (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          invoice_id INTEGER NOT NULL REFERENCES invoices(id),
          reference TEXT NOT NULL UNIQUE,
          amount TEXT NOT NULL,
          currency TEXT NOT NULL,
          provider TEXT NOT NULL,
          status TEXT NOT NULL CHECK(status IN ('pending','confirmed','rejected')),
          confirmed_by INTEGER REFERENCES users(id),
          confirmed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS notifications (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          channel TEXT NOT NULL,
          recipient TEXT NOT NULL,
          subject TEXT NOT NULL,
          body TEXT NOT NULL,
          status TEXT NOT NULL CHECK(status IN ('queued','sent','failed')),
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS files (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          owner_id INTEGER NOT NULL REFERENCES users(id),
          filename TEXT NOT NULL,
          object_key TEXT NOT NULL UNIQUE,
          sha256 TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS audit (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          actor_id INTEGER REFERENCES users(id),
          action TEXT NOT NULL,
          target_id TEXT NOT NULL,
          occurred_at TEXT NOT NULL
        );
        """)

def audit(db, user_id, action, target):
    from datetime import datetime, timezone
    db.execute("INSERT INTO audit(actor_id, action, target_id, occurred_at) VALUES (?,?,?,?)",
        (user_id, action, str(target), datetime.now(timezone.utc).isoformat()))
