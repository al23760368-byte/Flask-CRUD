from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models.users_rg import UsuariosRg
from models.libros_rg import LibrosRg
from utils.db import db
from models.resenas_rg import ResenasRg
from routes.auth import login_required

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/user", methods=["POST", "GET"])
@login_required
def user():
        libro = LibrosRg.query.all()
        return render_template("user.html", values=libro)

@user_bp.route("/api/reseñas-usuario", methods=["GET"])
@login_required
def obtener_reseñas_usuario():
    """Obtener todas las reseñas del usuario actual"""
    try:
        usuario_id = session.get('user_id')
        if not usuario_id:
            return jsonify({"error": "Usuario no autenticado"}), 401
        
        # Buscar todas las reseñas del usuario
        reseñas = ResenasRg.query.filter_by(usuario_id=usuario_id).all()
        
        # Formatear respuesta como diccionario {libro_id: datos}
        reseñas_dict = {}
        for reseña in reseñas:
            reseñas_dict[str(reseña.libro_id)] = {
                "calificacion": reseña.calificacion,
                "leido": reseña.leido,
                "fecha": reseña.fecha_creacion.isoformat() if reseña.fecha_creacion else None
            }
        
        return jsonify(reseñas_dict)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/api/guardar-reseña", methods=["POST"])
@login_required
def guardar_reseña():
    """Guardar o actualizar una reseña"""
    try:
        usuario_id = session.get('user_id')
        if not usuario_id:
            return jsonify({"error": "Usuario no autenticado"}), 401
        
        datos = request.get_json()
        
        # Validar datos
        if not datos or 'libro_id' not in datos:
            return jsonify({"error": "Datos incompletos"}), 400
        
        libro_id = datos.get('libro_id')
        calificacion = datos.get('calificacion', 0)
        leido = datos.get('leido', False)
        
        # Verificar que el libro exista
        libro = LibrosRg.query.get(libro_id)
        if not libro:
            return jsonify({"error": "Libro no encontrado"}), 404
        
        # Verificar si ya existe una reseña para este usuario y libro
        reseña_existente = ResenasRg.query.filter_by(
            usuario_id=usuario_id, 
            libro_id=libro_id
        ).first()
        
        if reseña_existente:
            # Actualizar reseña existente
            reseña_existente.calificacion = calificacion
            reseña_existente.leido = leido
            # No necesitas actualizar fecha_actualizacion manualmente, onupdate lo hace
            mensaje = "Reseña actualizada"
        else:
            # Crear nueva reseña
            nueva_reseña = ResenasRg(
                libro_id=libro_id,
                usuario_id=usuario_id,
                calificacion=calificacion,
                leido=leido
            )
            db.session.add(nueva_reseña)
            mensaje = "Reseña creada"
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "mensaje": mensaje,
            "libro_id": libro_id,
            "calificacion": calificacion,
            "leido": leido
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_bp.route("/api/reseña/<int:libro_id>", methods=["GET"])
@login_required
def obtener_reseña_libro(libro_id):
    """Obtener reseña específica para un libro"""
    try:
        usuario_id = session.get('user_id')
        if not usuario_id:
            return jsonify({"error": "Usuario no autenticado"}), 401
        
        reseña = ResenasRg.query.filter_by(
            usuario_id=usuario_id, 
            libro_id=libro_id
        ).first()
        
        if reseña:
            return jsonify({
                "calificacion": reseña.calificacion,
                "leido": reseña.leido,
                "fecha_creacion": reseña.fecha_creacion.isoformat() if reseña.fecha_creacion else None
            })
        else:
            return jsonify({
                "calificacion": 0,
                "leido": False
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ====== FUNCIÓN ORIGINAL QUE YA TENÍAS (la mantengo) ======

def save_review(user_id, book_id, calificacion):
    """Función original que ya tenías - la mantengo por compatibilidad"""
    nueva_resena = ResenasRg(libro_id=book_id, usuario_id=user_id, calificacion=calificacion)
    db.session.add(nueva_resena)
    db.session.commit()
    return nueva_resena

# ====== FUNCIÓN PARA ACTUALIZAR LA BASE DE DATOS ======

@user_bp.route("/actualizar-bd", methods=["GET"])
def actualizar_bd():
    """Ruta temporal para actualizar la estructura de la base de datos"""
    try:
        # Esto creará las tablas si no existen
        db.create_all()
        return "✅ Base de datos actualizada correctamente. Las tablas 'resenas' deberían tener ahora los campos 'leido', 'fecha_creacion' y 'fecha_actualizacion'."
    except Exception as e:
        return f"❌ Error: {str(e)}"