from functools import wraps
from flask import Blueprint,session, redirect, url_for
auth_bp=Blueprint("auth_login",__name__)
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper