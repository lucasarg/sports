from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired,Email, EqualTo, Length, NumberRange

# Clase que representa el formulario de login
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')


# Formulario de registro
class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[
        DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Registrarse')

class JugadorForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=2, max=100)])
    posicion = StringField("Posición", validators=[Length(max=50)])
    edad = IntegerField("Edad", validators=[NumberRange(min=0, max=120)])
    submit = SubmitField("Agregar jugador")
from wtforms import IntegerField

class EquipoForm(FlaskForm):
    nombre = StringField("Nombre del equipo", validators=[DataRequired(), Length(min=2, max=100)])
    ciudad = StringField("Ciudad", validators=[Length(max=100)])
    fundado_en = IntegerField("Año de fundación", validators=[NumberRange(min=1800, max=2100)])
    submit = SubmitField("Agregar equipo")
