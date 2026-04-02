from flask import Blueprint, render_template, request, redirect, session, flash
from services.utility import get_db, calculate_all
from services.auth_login import login_required

results_bp = Blueprint("results", __name__)


@results_bp.route("/add_result", methods=["GET", "POST"])
@login_required
def add_result():
    conn = get_db()

    if request.method == "POST":
        roll, branch = request.form["student"].split("|")

        marks = float(request.form["marks"])
        attendance = float(request.form["attendance"])
        semester = int(request.form["semester"])

        percentage, grade, performance, risk = calculate_all(
            marks, attendance, branch, semester
        )

        conn.execute("""
            INSERT INTO results
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        """, (roll, branch, semester, marks, attendance, percentage, grade, performance, risk,session['user_id']))

        conn.commit()
        flash("Semester Result added sucessfully")
        return redirect("/students")

    rows = conn.execute(
        "SELECT * FROM std_list WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    students = [dict(r) for r in rows]
    conn.close()

    return render_template("add_result.html", students=students)