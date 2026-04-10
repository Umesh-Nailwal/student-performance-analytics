from flask import Blueprint, render_template  ,request, redirect, session, flash, url_for
from services.utility import get_db, calculate_all,get_username
from services.auth_login import login_required

modify_bp=Blueprint("modify",__name__)

@modify_bp.route("/update/<roll>/<int:semester>", methods=["GET", "POST"])
@login_required
def update_result(roll, semester):
    conn = get_db()

    if request.method == "POST":
        marks = float(request.form["marks"])
        attendance = float(request.form["attendance"])
        
        student = conn.execute(
    "SELECT branch FROM std_list WHERE roll=?",
    (roll,)
).fetchone()

        branch = student["branch"]

        percentage, grade, performance, risk = calculate_all(marks, attendance,branch,semester)

        conn.execute("""
            UPDATE results
            SET marks=?, attendance=?, percentage=?, grade=?, performance=?, risk=?
            WHERE roll=?  AND branch=? AND semester=?
        """, (marks, attendance, percentage, grade, performance, risk, roll, branch,semester))

        conn.commit()
        conn.close()

        flash("Record updated successfully!", "success")
        return redirect(url_for("adv.student_detail", roll=roll))

    else:
        record = conn.execute("""
            SELECT * FROM results
            WHERE roll=? AND semester=?
        """, (roll, semester)).fetchone()

        conn.close()
        return render_template("edit.html", record=record)
  
@modify_bp.route("/delete/<roll>/<int:semester>")
@login_required
def delete_result(roll, semester):
    conn = get_db()

    conn.execute(
        "DELETE FROM results WHERE roll=? AND semester=?",
        (roll, semester)
    )

    conn.commit()
    conn.close()

    flash("Record deleted successfully!", "success")
    username=get_username()
    return redirect(url_for("adv.student_detail", roll=roll))
    