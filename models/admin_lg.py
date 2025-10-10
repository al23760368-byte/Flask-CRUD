from utils.db import db

class AdminLg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash