
import sqlite3
from flask import session
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ---------- DATABASE ----------

def get_db():
    db_path = "students.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_config_db():
    db_path = "config.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- CONFIG ----------

def get_total_marks(branch, semester,user_id):
    conn = get_config_db()
    data = conn.execute(
        "SELECT total_marks FROM config WHERE branch=? AND semester=? AND user_id=?",
        (branch, semester,user_id)
    ).fetchone()
    conn.close()
    return data["total_marks"] if data else 100


# ---------- CALCULATIONS ----------

def calculate_all(marks, attendance, branch=None, semester=None):
    total = 100

    if branch and semester:
        total = get_total_marks(branch, semester,session["user_id"])

    percentage = round((marks / total) * 100, 2)
    score = (percentage * 0.8) + (attendance * 0.2)

    # Grade
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 75:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    else:
        grade = "F"

    # Performance
    if score >= 85:
        performance = "Excellent"
    elif score >= 70:
        performance = "Good"
    elif score >= 50:
        performance = "Average"
    else:
        performance = "Poor"

    # Risk
    if score < 50:
        risk = "High"
    elif score < 65:
        risk = "Medium"
    else:
        risk = "Low"

    return percentage, grade, performance, risk
def get_username():
	user=session.get("username","Guest")
	return user