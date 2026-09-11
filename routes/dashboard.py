from flask import Blueprint, render_template, session
from services.utility import get_db
from services.auth_login import login_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def home():

    user_id = session["user_id"]
    conn = get_db()

    total = conn.execute(
        "SELECT COUNT(*) FROM std_list WHERE user_id=?",
        (user_id,)
    ).fetchone()[0]

    avg_pct = conn.execute("""
        SELECT ROUND(AVG(r.percentage), 2)
        FROM results r
        JOIN std_list s 
        ON r.student_id = s.id
        WHERE s.user_id=?
    """, (user_id,)).fetchone()[0] or 0

    avg_att = conn.execute("""
        SELECT ROUND(AVG(r.attendance), 2)
        FROM results r
        JOIN std_list s 
        ON r.student_id = s.id
        WHERE s.user_id=?
    """, (user_id,)).fetchone()[0] or 0

    high_risk_count = conn.execute("""
        SELECT COUNT(*)
        FROM results r
        JOIN std_list s 
        ON r.student_id = s.id 
        WHERE s.user_id=? AND r.risk='High'
    """, (user_id,)).fetchone()[0]

    top_students = conn.execute("""
        SELECT s.name, s.roll, MAX(r.percentage) as best
        FROM results r
        JOIN std_list s 
        ON r.student_id = s.id
        WHERE s.user_id=? AND (r.percentage)>80
        GROUP BY s.roll, s.branch 
        ORDER BY best DESC, semester
        LIMIT 7
    """, (user_id,)).fetchall()

    weak_students = conn.execute("""
        SELECT s.name, s.roll, MIN(r.percentage) as weak
        FROM results r
        JOIN std_list s 
        ON r.student_id = s.id 
        WHERE s.user_id=? AND (r.percentage)<70
        GROUP BY s.roll, s.branch
        ORDER BY weak ASC, semester
        LIMIT 7
    """, (user_id,)).fetchall()

    data = conn.execute("""
        SELECT semester, ROUND(AVG(r.percentage), 2) as avgp
        FROM results r
        JOIN std_list s 
        ON r.student_id = s.id
        WHERE s.user_id=?
        GROUP BY semester
    """, (user_id,)).fetchall()
    username=session.get("username","User")

    conn.close()

    semesters = [f"Sem {row['semester']}" for row in data]
    averages = [row["avgp"] for row in data]

    return render_template(
        "dashboard.html",
        total=total,
        semesters=semesters,
        averages=averages,
        top_students=top_students,
        weak_students=weak_students,
        avg_pct=avg_pct,
        avg_att=avg_att,
        high_risk_count=high_risk_count,
        username=username
    )