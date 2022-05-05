from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    """форма регистрации"""
    email = StringField('Электронная почта', validators=[Email()])
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeated_password = PasswordField('Повтор пароля', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    """форма логина"""
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class AddQuizForm(FlaskForm):
    """Форма добавления нового теста
    вопросы прилетают в форму в json"""
    name = StringField('Название теста', validators=[DataRequired()])
    description = TextAreaField('Описание')
    questions = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Добавить тест')