from flask import Blueprint, render_template, request, redirect, session, flash
from services.utility import get_db, get_username
from services.auth_login import login_required

student_bp = Blueprint("students", __name__)

# ---------------- STUDENTS ----------------

@student_bp.route("/students")
@login_required
def students():

    user_id = session["user_id"]
    search = request.args.get("search")
    year = request.args.get("year")
    branch = request.args.get("branch")

    conn = get_db()

    # BASE QUERY
    query = "SELECT * FROM std_list WHERE user_id=?"
    params = [user_id]

    # 🔥 Get all unique admission years
    years = conn.execute("""
        SELECT DISTINCT admission_year 
        FROM std_list 
        WHERE user_id=? 
        ORDER BY admission_year DESC
    """, (user_id,)).fetchall()

    # SEARCH
    if search:
        query += " AND (name LIKE ? OR roll LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")

    # YEAR FILTER
    if year:
        query += " AND admission_year=?"
        params.append(year)

    # BRANCH FILTER
    if branch:
        query += " AND branch=?"
        params.append(branch)

    # ✅ FIX: Add ORDER BY inside query
    query += " ORDER BY branch ASC,CAST( roll as INTEGER) ASC"

    # EXECUTE QUERY
    rows = conn.execute(query, params).fetchall()

    students = [dict(row) for row in rows]

    conn.close()
    username = get_username()

    return render_template(
        "student.html",
        students=students,
        years=years,
        username=username
    )


@student_bp.route("/add_student", methods=["GET", "POST"])
@login_required
def add_student():

    if request.method == "POST":
        user_id = session["user_id"]

        conn = get_db()
        conn.execute("""
            INSERT INTO std_list (roll, name, branch, admission_year, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.form["roll"],
            request.form["name"],
            request.form["branch"],
            request.form["admission_year"],
            user_id
        ))
        conn.commit()
        conn.close()

        flash("Student added successfully")

        return redirect("/students")

    username = get_username()
    return render_template("add_student.html", username=username)
