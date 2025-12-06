from utils.db import db

class UsuariosRg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)

    def __init__(self, usuario, contrasena):
        self.usuario = usuario
        self.contrasena = contrasena