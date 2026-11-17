import sqlite3
from contextlib import contextmanager

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL, price_cents INTEGER NOT NULL,
 stock INTEGER NOT NULL CHECK(stock >= 0));
CREATE TABLE IF NOT EXISTS orders (
 id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL,
 quantity INTEGER NOT NULL CHECK(quantity > 0), amount_cents INTEGER NOT NULL,
 status TEXT NOT NULL CHECK(status IN ('PENDING','PAID','FAILED')),
 payment_reference TEXT UNIQUE, FOREIGN KEY(product_id) REFERENCES products(id));
"""

def connect(path):
    con = sqlite3.connect(path, timeout=5, isolation_level=None)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys=ON')
    con.execute('PRAGMA busy_timeout=5000')
    return con

def init_db(path):
    with connect(path) as con:
        con.executescript(SCHEMA)
        con.execute('INSERT OR IGNORE INTO products(id,name,price_cents,stock) VALUES (1,?,?,?)', ('Carnet', 1200, 5))
        con.execute('INSERT OR IGNORE INTO products(id,name,price_cents,stock) VALUES (2,?,?,?)', ('Stylo', 350, 12))
