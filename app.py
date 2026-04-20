from flask import Flask 
from routes.students import student_bp
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.results import results_bp
from routes.admin_panel import admin_panel_bp
from routes.student_details import student_details_bp
from routes.filtered_list import filtered_list_bp
from routes.modify import modify_bp
from database.init_db import init_db
import os
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY","fallback_key")

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(student_bp)
app.register_blueprint(results_bp)
app.register_blueprint(modify_bp)
app.register_blueprint(admin_panel_bp)
app.register_blueprint(student_details_bp)
app.register_blueprint(filtered_list_bp)
# ---------------- RUN ----------------
init_db()

if __name__ == "__main__":
    app.run(debug=True)