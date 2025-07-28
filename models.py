from app import db

# ----------------------------------------
# 👤 User model
# ----------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


# ----------------------------------------
# ⚽ Player model
# ----------------------------------------
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    # Foreign key to reference the team the player belongs to
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    def __repr__(self):
        return f"<Player {self.name}>"


# ----------------------------------------
# 🏟️ Team model
# ----------------------------------------
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=True)

    # One-to-many relationship: a team has many players
    players = db.relationship('Player', backref='team', lazy=True)

    def __repr__(self):
        return f"<Team {self.name}>"
