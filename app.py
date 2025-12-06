import sys
import os

sys.path.append(os.path.dirname(__file__))

from flask import Flask
from routes.login import login_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.login_2 import login_2bp
from routes.auth import bp as auth_bp
from flask_sqlalchemy import SQLAlchemy
from routes.auth import login_required

app = Flask(__name__)
app.secret_key = "durazno22"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/mi_biblioteca"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(login_2bp)
app.register_blueprint(auth_bp)