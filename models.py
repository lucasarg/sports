from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.username}>"

class Jugador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    posicion = db.Column(db.String(50), nullable=True)
    edad = db.Column(db.Integer, nullable=True)

    # En el futuro: equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'))

    def __repr__(self):
        return f"<Jugador {self.nombre}>"

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=True)
    fundado_en = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Equipo {self.nombre}>"
