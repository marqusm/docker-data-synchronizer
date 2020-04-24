import os
import requests
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from app import configuration as cfg
from app import sql_statements as sql


def get_transmission_headers():
    response = requests.post(cfg.TRANSMISSION_API, data={"method": "session-stats"})
    session_id = response.headers[cfg.TRANSMISSION_SESSION_ID_HEADER]
    return {cfg.TRANSMISSION_SESSION_ID_HEADER: session_id}


def create_database_if_not_exists():
    if not os.path.exists(cfg.DATABASE_PATH):
        open(cfg.DATABASE_PATH, 'a+').close()
    conn = sqlite3.connect(cfg.DATABASE_PATH)
    c = conn.cursor()
    c.execute(sql.CREATE_TABLE)
    conn.commit()
    conn.close()


def add_processed_item(name, size):
    conn = sqlite3.connect(cfg.DATABASE_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO items (name, size, creation_date) VALUES ('{}', '{}', '{}')".format(name, size, datetime.now()))
    conn.commit()
    conn.close()


def get_processed_list(days_delta=cfg.CONSIDERING_HISTORY_DAYS):
    conn = sqlite3.connect(cfg.DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM items WHERE creation_date > '{}'".format(datetime.now() - timedelta(days=days_delta)))
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]


def cleanup_processed_list():
    if cfg.MAX_DAYS_DB_ENTRY < 0:
        return
    conn = sqlite3.connect(cfg.DATABASE_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE creation_date < DATETIME('now', '-{} day')".format(cfg.MAX_DAYS_DB_ENTRY))
    conn.commit()
    conn.close()


def get_size(path):
    size_in_b = sum([f.stat().st_size for f in Path(path).glob("**/*")])
    size_in_gb = size_in_b / 1024 ** 3
    return round(size_in_gb, 3)
