from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        from models import User  # Local import to avoid circular dependency
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        from models import User  # Local import to avoid circular dependency
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PickForm(FlaskForm):
    # Assuming each pick is a choice of a team from a game
    pick = SelectField('Pick a Team', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Submit Pick')

    def set_choices(self, games):
        """
        Set the choices for the pick field based on available games.
        :param games: A list of tuples, each representing a game.
                      Each tuple should be in the form (game_id, "Home Team vs Away Team")
        """
        self.pick.choices = games

class NewRoundForm(FlaskForm):
    game_date = DateField('Game Date', validators=[DataRequired()])
    home_team = StringField('Home Team', validators=[DataRequired()])
    away_team = StringField('Away Team', validators=[DataRequired()])
    submit = SubmitField('Create Game')



