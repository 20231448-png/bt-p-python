import sqlite3
from datetime import datetime

DB_NAME = "health_data.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            height REAL,
            weight REAL,
            bmi REAL,
            heart_rate INTEGER,
            co2 INTEGER,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def calculate_bmi(weight, height):
    h = height / 100
    return weight / (h * h)


def check_abnormal(bmi, heart_rate, co2):
    warnings = []

    if bmi < 18.5:
        warnings.append("BMI thấp")
    elif bmi >= 25:
        warnings.append("BMI cao")

    if heart_rate < 60:
        warnings.append("Nhịp tim thấp")
    elif heart_rate > 100:
        warnings.append("Nhịp tim cao")

    if co2 > 1000:
        warnings.append("CO2 cao")

    if warnings:
        return "Cảnh báo: " + ", ".join(warnings)

    return "Bình thường"


def insert_record(height, weight, heart_rate, co2):
    bmi = calculate_bmi(weight, height)
    status = check_abnormal(bmi, heart_rate, co2)
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO health_records
        (time, height, weight, bmi, heart_rate, co2, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (time, height, weight, bmi, heart_rate, co2, status))

    conn.commit()
    conn.close()

    return status


def get_all_records():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT time, height, weight, bmi, heart_rate, co2, status
        FROM health_records
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return rows


def get_latest_record():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT time, height, weight, bmi, heart_rate, co2, status
        FROM health_records
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()

    return row


def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*), AVG(bmi), AVG(heart_rate), AVG(co2)
        FROM health_records
    """)

    total, avg_bmi, avg_heart, avg_co2 = cur.fetchone()

    cur.execute("""
        SELECT COUNT(*)
        FROM health_records
        WHERE status != 'Bình thường'
    """)

    warning_count = cur.fetchone()[0]

    conn.close()

    return total, avg_bmi, avg_heart, avg_co2, warning_count