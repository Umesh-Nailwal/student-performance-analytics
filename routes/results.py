from flask import Blueprint, render_template, request, redirect, session, flash
from services.utility import get_db, calculate_all, get_username, get_config_db, get_total_marks
from services.auth_login import login_required

results_bp = Blueprint("results", __name__)

@results_bp.route("/add_result", methods=["GET", "POST"])
@login_required
def add_result():

    conn = get_db()
    user_id = session["user_id"]
    students=[]

    if request.method == "POST":

        student_id = int(request.form["student"])
        marks = float(request.form["marks"])
        attendance = float(request.form["attendance"])
        semester = int(request.form["semester"])

        try:
            student = conn.execute("""
            SELECT branch  FROM std_list
            WHERE id=? AND user_id=?
        """, [student_id, user_id]).fetchone()
            if not student:
                flash("Student not found")
                return redirect("/add_result")

            branch = student["branch"]
                 
            total_marks=get_total_marks(branch, semester,year,user_id)
        
            if marks < 0 or marks > total_marks:
                flash(f"Marks must be between 0 and {total_marks}")
                return redirect("/add_result")


       

            percentage, grade, performance, risk = calculate_all(marks, attendance, branch, semester)

            conn.execute("""
            INSERT INTO results (
                student_id,
                semester,
                marks,
                attendance,
                percentage,
                grade,
                performance,
                risk )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            semester,
            marks,
            attendance,
            percentage,
            grade,
            performance,
            risk
        ))

            conn.commit()
            conn.close()

            flash("Semester Result added successfully")
            return redirect("/students")

        except Exception as e:
            print("ERROR:", e)
            flash("Something went wrong. Please try again.")
            return redirect("/add_result")
            
    rows = conn.execute("""
        SELECT * FROM std_list
        WHERE user_id=?
        ORDER BY branch, roll
    """, [user_id]).fetchall()

    students = [dict(r) for r in rows]

    return render_template(
        "add_result.html",
        students=students,
        username=get_username()
    )