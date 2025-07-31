from flask_wtf import FlaskForm  # Base class for Flask-WTF forms
from wtforms import StringField, PasswordField, SubmitField, IntegerField,SelectField  # Basic form field types
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional  # Common validators

# ----------------------------------------
# 🔐 Login Form
# ----------------------------------------
class LoginForm(FlaskForm):
    # Username field, required
    username = StringField('User', validators=[DataRequired()])
    
    # Password field, required
    password = PasswordField('Password', validators=[DataRequired()])
    
    # Submit button
    submit = SubmitField('Submit')


# ----------------------------------------
# 📝 Registration Form
# ----------------------------------------
class RegisterForm(FlaskForm):
    # Username field, required
    username = StringField('User', validators=[DataRequired()])
    
    # Email field, must be a valid email format
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Password field, required
    password = PasswordField('Password', validators=[DataRequired()])
    
    # Confirmation password, must match 'password'
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must be the same')
    ])
    
    # Submit button
    submit = SubmitField('Register')


# ----------------------------------------
# ⚽ Player Form
# ----------------------------------------
class PlayerForm(FlaskForm):
    # Name field, required, with length between 2 and 100 characters
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=100)])
    
    # Position field, optional, with a max length of 50
    position = StringField("Position", validators=[Length(max=50)])
    
    # Age field, must be between 0 and 120
    age = IntegerField("Age", validators=[NumberRange(min=0, max=120)])

    team_id = SelectField('Team', coerce=int, validators=[Optional()])
    
    # Submit button
    submit = SubmitField("Submit")


# ----------------------------------------
# 🏟️ Team Form
# ----------------------------------------
class TeamForm(FlaskForm):
    # Team name, required, between 2 and 100 characters
    name = StringField("Team name", validators=[DataRequired(), Length(min=2, max=100)])
    
    # City name, optional, max 100 characters
    city = StringField("City", validators=[Length(max=100)])

    # Submit button
    submit = SubmitField("Add team")
