from flask import Blueprint, render_template, request, redirect, url_for
from models.libros_rg import LibrosRg
from utils.db import db

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route("/admin", methods=["POST", "GET"])
def admin():

    query = request.args.get('q', '').strip()

    if request.method == "POST":
        id_libro = request.form["id_libro"]
        titulo=request.form["titulo"]
        autor=request.form["autor"]
        anio_publicacion=request.form["anio_publicacion"]
        genero=request.form["genero"]
        descripcion=request.form.get("descripcion","")

        if id_libro:
            libro_edit = LibrosRg.query.get(id_libro)
            if libro_edit:
                libro_edit.titulo = titulo
                libro_edit.autor = autor
                libro_edit.anio_publicacion = anio_publicacion
                libro_edit.genero = genero
                libro_edit.descripcion = descripcion
        else:
            nuevo_libro = LibrosRg(titulo, autor, anio_publicacion, genero, descripcion)
            db.session.add(nuevo_libro)
        db.session.commit()    
        return redirect("/admin")

    if query:
        libro = LibrosRg.query.filter(
            (LibrosRg.titulo.ilike(f'%{query}%')) | 
            (LibrosRg.autor.ilike(f'%{query}%'))
        ).all()    
    else:
        libro = LibrosRg.query.all()

    return render_template("admin.jinja", values=libro)

@admin_bp.route("/admin/eliminar/<int:id>")
def eliminar(id):
    libro_del = LibrosRg.query.get(id)
    if libro_del:
        db.session.delete(libro_del)
        db.session.commit()
    return redirect(url_for('admin_bp.admin'))

@admin_bp.route("/admin/prueba")
def prueba():
    libro = LibrosRg.query.all()
    return render_template("prueba.html", values=libro)