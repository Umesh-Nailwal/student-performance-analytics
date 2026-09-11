from flask import Blueprint, render_template  ,request, redirect, session, flash, url_for
from services.utility import get_db, calculate_all,get_username, get_config_db
from services.auth_login import login_required

modify_bp=Blueprint("modify",__name__)

@modify_bp.route("/update/<int:student_id>/<int:semester>", methods=["GET", "POST"])
@login_required
def update_result(student_id, semester):

    conn = get_db()

    student = conn.execute("""
        SELECT branch, roll, admission_year
        FROM std_list
        WHERE id=?
    """, [student_id]).fetchone()

    if not student:
        conn.close()
        flash("Student not found")
        return redirect("/students")

    branch = student["branch"]
    roll = student["roll"]
    admission_year = student["admission_year"]

    if request.method == "POST":

        marks = float(request.form["marks"])
        attendance = float(request.form["attendance"])

        
        if attendance < 0 or attendance > 100:
            flash("Attendance must be between 0 and 100")
            return redirect(url_for("modify.update_result",
                student_id=student_id,
                semester=semester))

        percentage, grade, performance, risk = calculate_all(
            marks, attendance, branch, semester,
        )

        conn.execute("""
            UPDATE results
            SET marks=?, attendance=?, percentage=?, grade=?, performance=?, risk=?
            WHERE student_id=? AND semester=?
        """, (
            marks, attendance, percentage, grade,
            performance, risk, student_id, semester
        ))

        conn.commit()
        conn.close()

        flash("Record updated successfully!", "success")

        return redirect(url_for(
            "adv.student_detail",
            roll=roll,
            branch=branch,
            admission_year=admission_year
        ))

    record = conn.execute("""
        SELECT * FROM results
        WHERE student_id=? AND semester=? 
    """, [student_id, semester]).fetchone()

    conn.close()

    return render_template("edit.html", record=record)

@modify_bp.route("/delete/<int:student_id>/<int:semester>")
@login_required
def delete_result(student_id, semester):

    conn = get_db()

    student = conn.execute("""
        SELECT roll, branch, admission_year
        FROM std_list
        WHERE id=?
    """, [student_id]).fetchone()

    if not student:
        conn.close()
        flash("Student not found")
        return redirect("/students")

    conn.execute("""
        DELETE FROM results
        WHERE student_id=? AND semester=?
    """, [student_id, semester])

    conn.commit()
    conn.close()

    flash("Record deleted successfully!", "success")

    return redirect(url_for(
        "adv.student_detail",
        roll=student["roll"],
        branch=student["branch"],
        admission_year=student["admission_year"]
    ))    