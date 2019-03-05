from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, NumberRange
from gymbo.models import User, Lift
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=30)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        #If user is found in db, raise error
        if user:
            raise ValidationError('Username is already registered')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        #If user is found in db, raise error
        if user:
            raise ValidationError('Email is already registered')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=30)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            #If user is found in db, raise error
            if user:
                raise ValidationError('Username is already registered')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            #If email is found in db, raise error
            if user:
                raise ValidationError('Email is already registered')

class UpdateLiftForm(FlaskForm):
    bench_id = Lift.query.filter_by(lift='bench').first().id
    squat_id = Lift.query.filter_by(lift='squat').first().id
    front_squat_id = Lift.query.filter_by(lift='front_squat').first().id
    deadlift_id = Lift.query.filter_by(lift='deadlift').first().id
    bench_press = IntegerField('Bench Press', validators=[InputRequired(), NumberRange(min=0)])
    squat = IntegerField('Squat', validators=[InputRequired(), NumberRange(min=0)])
    front_squat = IntegerField('Front Squat', validators=[InputRequired(), NumberRange(min=0)])
    deadlift = IntegerField('Deadlift', validators=[InputRequired(), NumberRange(min=0)])
    submit = SubmitField('Update')
