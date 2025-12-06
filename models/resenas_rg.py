from utils.db import db
from datetime import datetime

class ResenasRg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros_rg.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios_rg.id'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False, default=0)  # 0-5, 0 = sin valorar
    leido = db.Column(db.Boolean, default=False)  # Nuevo campo: True = Leído, False = No Leído
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)  # Nuevo campo
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Nuevo campo

    def __init__(self, libro_id, usuario_id, calificacion=0, leido=False):
        self.libro_id = libro_id
        self.usuario_id = usuario_id
        self.calificacion = calificacion
        self.leido = leido

    def __repr__(self):
        return f'<Resena Libro:{self.libro_id} Usuario:{self.usuario_id} Cal:{self.calificacion} Leido:{self.leido}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario para JSON"""
        return {
            'id': self.id,
            'libro_id': self.libro_id,
            'usuario_id': self.usuario_id,
            'calificacion': self.calificacion,
            'leido': self.leido,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }