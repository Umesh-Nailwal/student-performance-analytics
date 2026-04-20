"""
services/student_queries.py
All DB queries related to students and results.
Routes call these functions — no raw SQL in route files.
"""
from services.utility import get_db, get_config_db, calculate_all
from flask import session


# ───────────────────────── STUDENTS ─────────────────────────

def get_all_students(user_id, search=None, year=None, branch=None):
    conn = get_db()
    query = "SELECT * FROM std_list WHERE user_id=?"
    params = [user_id]
    if search:
        query += " AND (name LIKE ? OR roll LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    if year:
        query += " AND admission_year=?"
        params.append(year)
    if branch:
        query += " AND branch=?"
        params.append(branch)
    query += " ORDER BY branch ASC, CAST(roll AS INTEGER) ASC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_distinct_years(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT admission_year FROM std_list WHERE user_id=? ORDER BY admission_year DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_distinct_branches(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT branch FROM std_list WHERE user_id=?",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def insert_student(roll, name, branch, admission_year, user_id):
    conn = get_db()
    conn.execute(
        "INSERT INTO std_list (roll, name, branch, admission_year, user_id) VALUES (?, ?, ?, ?, ?)",
        (roll, name, branch, admission_year, user_id)
    )
    conn.commit()
    conn.close()


def get_student_by_roll(roll):
    conn = get_db()
    row = conn.execute("SELECT * FROM std_list WHERE roll=?", (roll,)).fetchone()
    conn.close()
    return row


# ───────────────────────── RESULTS ─────────────────────────

def get_results_by_roll(roll):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM results WHERE roll=? ORDER BY semester ASC", (roll,)
    ).fetchall()
    conn.close()
    return rows


def get_avg_percentage_by_roll(roll):
    conn = get_db()
    val = conn.execute(
        "SELECT ROUND(AVG(percentage),2) FROM results WHERE roll=?", (roll,)
    ).fetchone()[0]
    conn.close()
    return val


def get_total_semesters_by_roll(roll):
    conn = get_db()
    val = conn.execute(
        "SELECT MAX(semester) FROM results WHERE roll=?", (roll,)
    ).fetchone()[0]
    conn.close()
    return val


def insert_result(roll, branch, semester, marks, attendance, admission_year, user_id):
    percentage, grade, performance, risk = calculate_all(marks, attendance, branch, semester)
    conn = get_db()
    conn.execute(
        "INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (roll, branch, semester, marks, attendance, percentage, grade, performance, risk, user_id, admission_year)
    )
    conn.commit()
    conn.close()


def update_result(roll, branch, semester, marks, attendance):
    percentage, grade, performance, risk = calculate_all(marks, attendance, branch, semester)
    conn = get_db()
    conn.execute(
        "UPDATE results SET marks=?, attendance=?, percentage=?, grade=?, performance=?, risk=? WHERE roll=? AND branch=? AND semester=?",
        (marks, attendance, percentage, grade, performance, risk, roll, branch, semester)
    )
    conn.commit()
    conn.close()


def delete_result(roll, semester):
    conn = get_db()
    conn.execute("DELETE FROM results WHERE roll=? AND semester=?", (roll, semester))
    conn.commit()
    conn.close()


def get_result_by_roll_semester(roll, semester):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM results WHERE roll=? AND semester=?", (roll, semester)
    ).fetchone()
    conn.close()
    return row


def get_filtered_results(user_id, semester=None, branch=None, year=None, search=None):
    conn = get_db()
    query = """
        SELECT s.name, s.admission_year, r.*
        FROM results r
        JOIN std_list s ON r.roll = s.roll AND r.branch = s.branch
        WHERE s.user_id=?
    """
    params = [user_id]
    if semester:
        query += " AND r.semester=?"
        params.append(semester)
    if branch:
        query += " AND r.branch=?"
        params.append(branch)
    if year:
        query += " AND s.admission_year=?"
        params.append(year)
    if search:
        query += " AND s.name LIKE ?"
        params.append(f"%{search}%")
    query += " ORDER BY r.semester ASC"
    rows = conn.execute(query, tuple(params)).fetchall()
    conn.close()
    return rows


# ───────────────────────── DASHBOARD ─────────────────────────

def get_dashboard_stats(user_id):
    conn = get_db()

    total = conn.execute(
        "SELECT COUNT(*) FROM std_list WHERE user_id=?", (user_id,)
    ).fetchone()[0]

    avg_pct = conn.execute("""
        SELECT ROUND(AVG(r.percentage), 2)
        FROM results r JOIN std_list s ON r.roll = s.roll AND r.branch = s.branch
        WHERE s.user_id=?
    """, (user_id,)).fetchone()[0] or 0

    avg_att = conn.execute("""
        SELECT ROUND(AVG(r.attendance), 2)
        FROM results r JOIN std_list s ON r.roll = s.roll AND r.branch = s.branch
        WHERE s.user_id=?
    """, (user_id,)).fetchone()[0] or 0

    high_risk = conn.execute("""
        SELECT COUNT(*) FROM results r
        JOIN std_list s ON r.roll = s.roll AND r.branch = s.branch
        WHERE s.user_id=? AND r.risk='High'
    """, (user_id,)).fetchone()[0]

    top_students = conn.execute("""
        SELECT s.name, r.roll, MAX(r.percentage) as best
        FROM results r JOIN std_list s ON r.roll = s.roll AND r.branch = s.branch
        WHERE s.user_id=? GROUP BY r.roll, r.branch ORDER BY best DESC LIMIT 5
    """, (user_id,)).fetchall()

    weak_students = conn.execute("""
        SELECT s.name, r.roll, MAX(r.percentage) as best
        FROM results r JOIN std_list s ON r.roll = s.roll AND r.branch = s.branch
        WHERE s.user_id=? GROUP BY r.roll, r.branch ORDER BY best ASC LIMIT 5
    """, (user_id,)).fetchall()

    chart_data = conn.execute("""
        SELECT semester, ROUND(AVG(r.percentage), 2) as avgp
        FROM results r JOIN std_list s ON r.roll = s.roll AND r.branch = s.branch
        WHERE s.user_id=? GROUP BY semester
    """, (user_id,)).fetchall()

    conn.close()
    return total, avg_pct, avg_att, high_risk, top_students, weak_students, chart_data


# ───────────────────────── CONFIG ─────────────────────────

def get_configs(user_id):
    conn = get_config_db()
    rows = conn.execute("SELECT * FROM config WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return rows


def upsert_config(branch, semester, total_marks, user_id, admission_year=None):
    conn = get_config_db()
    conn.execute(
        "INSERT OR REPLACE INTO config VALUES (?, ?, ?, ?, ?)",
        (branch, semester, total_marks, admission_year, user_id)
    )
    conn.commit()
    conn.close()


def remove_config(branch, semester, user_id):
    conn = get_config_db()
    conn.execute(
        "DELETE FROM config WHERE branch=? AND semester=? AND user_id=?",
        (branch, semester, user_id)
    )
    conn.commit()
    conn.close()


# ───────────────────────── AUTH ─────────────────────────

def get_user_by_username(username):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return user


def create_user(username, hashed_password):
    conn = get_db()
    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()
