from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from  wtforms.validators import Email, DataRequired, EqualTo, Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=5,max=18)])
    email = StringField('Email',validators=[Email(),DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=8,max=25)])
    confirm_password = PasswordField('Confirm Password',validators=[EqualTo('password'),DataRequired()])
    submit = SubmitField('Signup')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=18)])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=8,max=25)])
    submit = SubmitField('Login')
