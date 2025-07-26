from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.utils import login_requerido
from app.models import Usuario
from app.forms import JugadorForm
from app.forms import EquipoForm
from app import db


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("index.html")

@main.route('/perfil')
@login_requerido
def perfil():
    usuario = Usuario.query.get(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario)


from app.models import Jugador
from flask import render_template

@main.route("/jugadores")
def ver_jugadores():
    jugadores = Jugador.query.all()
    return render_template("jugadores.html", jugadores=jugadores)


@main.route("/agregar-jugador", methods=["GET", "POST"])
def agregar_jugador():
    form = JugadorForm()
    if form.validate_on_submit():
        nuevo_jugador = Jugador(
            nombre=form.nombre.data,
            posicion=form.posicion.data,
            edad=form.edad.data
        )
        db.session.add(nuevo_jugador)
        db.session.commit()
        flash(f"Jugador {nuevo_jugador.nombre} agregado correctamente ✅", "success")
        return redirect(url_for("main.ver_jugadores"))

    return render_template("agregar_jugador.html", form=form)

from app.models import Equipo

@main.route("/equipos")
def ver_equipos():
    equipos = Equipo.query.all()
    return render_template("equipos.html", equipos=equipos)


@main.route("/agregar-equipo", methods=["GET", "POST"])
def agregar_equipo():
    form = EquipoForm()
    if form.validate_on_submit():
        nuevo_equipo = Equipo(
            nombre=form.nombre.data,
            ciudad=form.ciudad.data,
            fundado_en=form.fundado_en.data
        )
        db.session.add(nuevo_equipo)
        db.session.commit()
        flash(f"Equipo {nuevo_equipo.nombre} agregado correctamente ✅", "success")
        return redirect(url_for("main.ver_equipos"))
    
    return render_template("agregar_equipo.html", form=form)
