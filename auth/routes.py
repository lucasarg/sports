from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.models import Usuario               # Modelo de la tabla 'usuarios'
from app import db                          # Objeto de la base de datos SQLAlchemy
from werkzeug.security import generate_password_hash , check_password_hash # Para encriptar contraseñas
from app.forms import LoginForm, RegisterForm         # Formularios de login y registro


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data  # Capturamos lo que el usuario escribió
        password = form.password.data

        # Buscamos el usuario en la base de datos
        usuario = Usuario.query.filter_by(username=username).first()

        # Verificamos si el usuario existe y la contraseña es correcta
        if usuario and check_password_hash(usuario.password, password):
            session['usuario_id'] = usuario.id   # ← Este es el "inicio real de sesión"
            flash(f'Bienvenido {usuario.username} 👋', 'success')
            return redirect(url_for('main.home'))  # Redirigimos a la página principal
        else:
            flash('Credenciales incorrectas ❌', 'danger')  # Mostramos error

    # Si no se envió el formulario o hay errores, se vuelve a mostrar
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Encriptamos la contraseña antes de guardarla
        hashed_password = generate_password_hash(password)

        # Creamos el objeto Usuario
        nuevo_usuario = Usuario(username=username, email=email, password=hashed_password)

        # Lo agregamos a la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('¡Registro exitoso! Ya podés iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/logout')
def logout():
    session.pop('usuario_id', None)  # Eliminamos la clave de sesión
    flash('Sesión cerrada correctamente 👋', 'info')
    return redirect(url_for('auth.login'))
