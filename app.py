from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

from services.utility import  get_db,calculate_all

from services.auth_login import login_required

from routes.students import student_bp
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.results import results_bp
from database.init_db import init_db
from routes.admin_panel import admin_panel_bp
from routes.student_details import student_details_bp
from routes.filtered_list import filtered_list_bp
from routes.modify import modify_bp
app = Flask(__name__)
app.secret_key = "super_secret_key_123"

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(student_bp)
app.register_blueprint(results_bp)
app.register_blueprint(modify_bp)
app.register_blueprint(admin_panel_bp)
app.register_blueprint(student_details_bp)
app.register_blueprint(filtered_list_bp)
#-------- INITIALIZE DATABASE
init_db()
# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)