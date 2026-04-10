from flask import (
    Blueprint, render_template,
    request, session
)
from services.utility import get_db,get_username
from services.auth_login import login_required

filtered_list_bp = Blueprint("filtered", __name__)

# ------ Semester wise results ------
@filtered_list_bp.route("/semester-results")
@login_required
def semester_results():

    user_id = session["user_id"]

    # 🔥 Get filters
    semester = request.args.get("semester")
    branch = request.args.get("branch")
    year = request.args.get("year")
    search = request.args.get("search")

    conn = get_db()

    # 🔥 Base query
    query = """
        SELECT s.name, s.admission_year, r.*
        FROM results r
        JOIN std_list s 
        ON r.roll = s.roll AND r.branch = s.branch
        WHERE s.user_id=?
    """

    params = [user_id]

    # 🔥 Apply filters dynamically

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
        params.append('%' + search + '%')

    # 🔥 Sorting
    query += " ORDER BY r.semester ASC"

    results = conn.execute(query, tuple(params)).fetchall()

    # 🔥 Get dropdown data (dynamic filters)
    years = conn.execute("""
        SELECT DISTINCT admission_year 
        FROM std_list 
        WHERE user_id=?
        ORDER BY admission_year DESC
    """, (user_id,)).fetchall()

    branches = conn.execute("""
        SELECT DISTINCT branch 
        FROM std_list 
        WHERE user_id=?
    """, (user_id,)).fetchall()

    conn.close()
    username=get_username()
    return render_template(
        "semester_results.html",
        results=results,
        years=years,
        branches=branches,
        username=username
    )