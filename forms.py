from wtforms import SelectField, StringField, PasswordField, IntegerField, TextField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email

class SignupForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=20)])
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])
    location = StringField('Zip-code or City', validators=[InputRequired()])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])

class EditUserForm(FlaskForm):
    """Edit User."""

    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    image_url = StringField('Image URL')
    location = TextField('Location')
    password = PasswordField('Password', validators=[Length(min=6, max=20)])

class SearchPlantForm(FlaskForm):
    """Search api for plants matching"""

    name = StringField('Name', validators=[InputRequired()])

class AddGardenForm(FlaskForm):
    """Add a new garden"""

    name = StringField('Name', validators=[InputRequired(), Length(min=3, max=15)])
    description = TextField('Description', validators=[Length(max=100)])

class AddPlantToGardenForm(FlaskForm):
    """Drop down form that adds plant to garden"""

    garden = SelectField('', validate_choice=False)