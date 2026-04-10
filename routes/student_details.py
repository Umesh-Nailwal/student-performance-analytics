from flask import Blueprint, render_template 
from services.utility import get_db,get_username
from services.auth_login import login_required

student_details_bp=Blueprint("adv",__name__)
# ---------------- STUDENT DETAIL (ADVANCED RISK AI LOGIC) ----------------

@student_details_bp.route("/student/<roll>")
@login_required
def student_detail(roll):
    conn = get_db()

    student = conn.execute(
        "SELECT * FROM std_list WHERE roll=?",
        (roll,)
    ).fetchone()

    results = conn.execute("""
        SELECT * FROM results
        WHERE roll=?
        ORDER BY semester ASC
    """, (roll,)).fetchall()
    
    avg_pct= conn.execute("""
    SELECT ROUND( AVG(percentage),2) FROM results
    WHERE roll=?
    """,(roll,)).fetchone()[0]
    
    total_sem= conn.execute("""
    SELECT MAX(semester) FROM results
    WHERE roll=?
   """,(roll,) ).fetchone()[0]

    conn.close()

    percentages = [r["percentage"] for r in results]
    attendances = [r["attendance"] for r in results]

    risk_score = 0
    insights = []

    if percentages:
        latest_percentage = percentages[-1]
        latest_attendance = attendances[-1]

        performance_score = (latest_percentage * 0.8) + (latest_attendance * 0.2)

        # 1️⃣ Low performance
        if performance_score < 60:
            risk_score += 2
            insights.append("Overall performance below safe threshold.")

        # 2️⃣ Two consecutive decline
        if len(percentages) >= 3:
            if (percentages[-1] < percentages[-2] and
                percentages[-2] < percentages[-3]):
                risk_score += 2
                insights.append("Two consecutive semesters declining.")

        # 3️⃣ Sharp drop >20
        if len(percentages) >= 2:
            if (percentages[-2] - percentages[-1]) > 20:
                risk_score += 2
                insights.append("Sharp drop greater than 20% detected.")

        # 4️⃣ Unstable fluctuation
        if (max(percentages) - min(percentages)) > 30:
            risk_score += 1
            insights.append("Performance instability detected.")

        # 5️⃣ Low attendance
        if latest_attendance < 65:
            risk_score += 1
            insights.append("Attendance below recommended level.")

        # Final decision
        if risk_score >= 5:
            final_risk = "High"
        elif risk_score >= 3:
            final_risk = "Medium"
        else:
            final_risk = "Low"

        # Override rule
        if performance_score < 60:
            final_risk = "High"

    else:
        final_risk = "Low"
    username=get_username()

    return render_template(
        "student_detail.html",
        student=student,
        results=results,
        insights=insights,
        final_risk=final_risk,
        avg_pct=avg_pct,
        total_sem=total_sem,
        username=username
    )
