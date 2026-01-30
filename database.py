import sqlite3
from datetime import datetime, timedelta

def create_db():
    conn = sqlite3.connect("phishing.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            prediction TEXT,
            phishing_score REAL,
            legit_score REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_scan(url, prediction, phishing_score, legit_score, timestamp):
    conn = sqlite3.connect("phishing.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO scans (url, prediction, phishing_score, legit_score, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (url, prediction, phishing_score, legit_score, timestamp))
    conn.commit()
    conn.close()


def get_all_scans():
    conn = sqlite3.connect("phishing.db")
    c = conn.cursor()
    c.execute("SELECT * FROM scans ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows


# ------------------------------------------------
#        DELETE ONE RECORD
# ------------------------------------------------
def delete_record_by_id(record_id):
    conn = sqlite3.connect("phishing.db")
    c = conn.cursor()
    c.execute("DELETE FROM scans WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


# ------------------------------------------------
#        DELETE ALL RECORDS
# ------------------------------------------------
def delete_all_records():
    conn = sqlite3.connect("phishing.db")
    c = conn.cursor()
    c.execute("DELETE FROM scans")
    conn.commit()
    conn.close()


# ------------------------------------------------
#   DELETE RECORDS OLDER THAN X DAYS
# ------------------------------------------------
def delete_old_records(days):
    conn = sqlite3.connect("phishing.db")
    c = conn.cursor()

    # Convert number of days to date
    cutoff_date = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff_date.strftime("%Y-%m-%d %H:%M:%S")

    c.execute("DELETE FROM scans WHERE timestamp < ?", (cutoff_str,))
    conn.commit()
    conn.close()
