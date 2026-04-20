from flask import (
Blueprint, render_template,
flash,request,session, redirect, url_for
)
from services.utility import get_config_db, get_db, get_username
from services.auth_login import login_required
admin_panel_bp =Blueprint("admin_panel",__name__)

@admin_panel_bp.route("/admin-panel", methods=["GET", "POST"])
@login_required
def admin_panel():
    conn = get_config_db()
    if request.method == "POST":
        conn.execute("""
            INSERT OR REPLACE INTO config
            VALUES (?, ?, ?,?)
        """, (
            request.form["branch"],
            request.form["semester"],
            request.form["total_marks"],
            session["user_id"]
        ))
        conn.commit()
        
        conn.close()
       

        flash("Saved!", "success")
    configs = conn.execute("SELECT * FROM config WHERE user_id=?", (session["user_id"],)).fetchall()
    username=get_username()


    return render_template("admin_pannel.html", configs=configs,username=username)

@admin_panel_bp.route("/delete-config/<branch>/<int:semester>")
@login_required
def delete_config(branch, semester):
    conn = get_config_db()

    conn.execute("""
        DELETE FROM config
        WHERE branch=? AND semester=? AND user_id=?
    """, (branch, semester, session["user_id"]))

    conn.commit()
    conn.close()

    flash("Configuration deleted!", "success")
    return redirect(url_for("admin_panel.admin_panel"))
