from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField
#from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    """форма регистрации"""
    login = StringField('Введи почту', validators=[DataRequired()])
    password = PasswordField('Введи пароль', validators=[DataRequired()])
    confirm = PasswordField('Повтори-ка', validators=[DataRequired()])
    surname = StringField('Твоя фамилия, ведьма', validators=[DataRequired()])
    name = StringField('Твоё имя, ведьма', validators=[DataRequired()])
    submit = SubmitField('Отправить вселенной')


class LoginForm(FlaskForm):
    """форма авторизации"""
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Закрепиться в памяти')
    submit = SubmitField('Постучаться в космос')