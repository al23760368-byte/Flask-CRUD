import sys
import os

sys.path.append(os.path.dirname(__file__))

from flask import Flask
from routes.login import login_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.login_2 import login_2bp
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/mi_biblioteca"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(login_2bp)