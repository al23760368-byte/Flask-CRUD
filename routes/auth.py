from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.users_rg import UsuariosRg
from utils.db import db
# Funcion para agregar decoradores
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')
@bp.route('/register', methods=["POST", "GET"])
def reglog():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]

        nuevo_usuario = UsuariosRg(usuario, contrasena)
        db.session.add(nuevo_usuario)
        db.session.commit()    
        return redirect(url_for('auth.reglog'))

    return render_template("reglog.html")

@bp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]

        usuario_encontrado = UsuariosRg.query.filter_by(usuario=usuario, contrasena=contrasena).first()
        if usuario_encontrado:
            session.clear()
            session['user_id'] = usuario_encontrado.id
            session['usuario'] = usuario_encontrado.usuario
            return redirect(url_for('user_bp.user'))
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for('auth.reglog'))

    return redirect(url_for('auth.reglog'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.reglog'))

# Login required decorador para proteger rutas
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view