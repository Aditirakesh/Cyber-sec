"""Shared DB helper. Each module gets its OWN sqlite file, so nobody
depends on anyone else's tables.  Usage inside a module:

    from db import get_conn
    conn = get_conn("sqli")      # creates data/sqli.db on first use
"""
import os
import sqlite3

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def get_conn(name: str) -> sqlite3.Connection:
    conn = sqlite3.connect(os.path.join(DATA_DIR, f"{name}.db"))
    conn.row_factory = sqlite3.Row
    return conn
