from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password",
                              validators=[DataRequired(),
                                          EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class TrialForm(FlaskForm):
    chosen_bin = StringField()

    def validate_chosen_bin(self, chosen_bin):
        if len(chosen_bin.data) < 3:
            raise ValidationError("Please choose a bin")
        if not (chosen_bin.data[0] == "b"):
            raise ValidationError("Please choose a bin")

    submit_trial = SubmitField("Next Trial")


class ClearTrialForm(FlaskForm):
    submit_trial = SubmitField("Clear all Trials")

class ConsentForm(FlaskForm):
    submit_consent = SubmitField("I have read and understood the information above and want to participate in this research.")

class TrainingForm(FlaskForm):
    submit_training = SubmitField("Got it, I'm ready to begin!")

class DemoForm(FlaskForm):
    submit_demo = SubmitField("Next Demonstration")

class ClearDemoForm(FlaskForm):
    submit_demo = SubmitField("Clear all Demos")