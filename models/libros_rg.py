from utils.db import db

class LibrosRg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    anio_publicacion = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    def __init__(self, titulo, autor, anio_publicacion, genero, descripcion):
        self.titulo = titulo
        self.autor = autor
        self.anio_publicacion = anio_publicacion
        self.genero = genero
        self.descripcion = descripcion