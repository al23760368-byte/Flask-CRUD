from flask import Blueprint, render_template

login_2bp = Blueprint('login_2bp', __name__)

@login_2bp.route("/login")
def home():
    return render_template("login_2.html")