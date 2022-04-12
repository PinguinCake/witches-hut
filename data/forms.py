from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField
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


class RecoveryForm(FlaskForm):
    """форма восстановления пароля"""
    name = StringField('Твоё имя, ведьма', validators=[DataRequired()])
    email = StringField('Введи почту', validators=[DataRequired()])
    submit = SubmitField('Отправить воспоминание')


class FinalRecoveryForm(FlaskForm):
    """форма восстановления пароля"""
    email = StringField('Введи почту', validators=[DataRequired()])
    password = PasswordField('Введи новый пароль', validators=[DataRequired()])
    submit = SubmitField('Отправить воспоминание')


class ZodiacsForm(FlaskForm):
    """форма выбора знаков зодиака"""
    his_sign = SelectField('Его знак зодиака', validators=[DataRequired()])
    her_sign = SelectField('Её знак зодиака', validators=[DataRequired()])
    submit = SubmitField('Узнать совместимость (%)')


class NamesForm(FlaskForm):
    """форма выбора имён"""
    his_name = StringField('Его имя', validators=[DataRequired()])
    her_name = StringField('Её имя', validators=[DataRequired()])
    submit = SubmitField('Узнать совместимость (%)')
