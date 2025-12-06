from flask import Blueprint, render_template, request, redirect, url_for
from models.users_rg import UsuariosRg
from utils.db import db

login_2bp = Blueprint('login_2bp', __name__)
usuarios = []

@login_2bp.route("/login", methods=["POST", "GET"])
def home():

    if request.method == "POST":
        usuario = request.form["usuario"]
        usuarios.append(usuario)
        print("este es el usuario: " + usuario)

    saludo = "hola"

    return render_template("login_2.html",  value = usuarios)
