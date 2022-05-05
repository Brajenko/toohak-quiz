from toohak.forms import RegisterForm
from flask import flash
import string


def contains_whitespace(s):
    return True in [c in s for c in string.whitespace]


def check_password_form(password, rep_password):
    """Проверка надежности пароля"""
    errors_password = 0
    if (len(password) < 4 or len(password) > 60) or (contains_whitespace(password) is True) or (
            password != rep_password):
        if len(password) < 4 or len(password) > 60:
            # длинна пароля
            errors_password += 1
            flash('Ошибка: длина пароля не может быть меньше 4 или больше 60 символов. '
                  'Минимально рекомендуемая длина пароля — в пределах от 12 до 14 символов.', 'error')
        if contains_whitespace(password) is True:
            # пустые символы в пароле
            errors_password += 1
            flash('Ошибка: в поле пароля не может быть пробелов', 'error')
        if password != rep_password:
            # пароли не совпадают
            errors_password += 1
            flash('Ошибка: поле пароля не совпадает с полем повтора пароля.', 'error')
    return errors_password


def check_form(form: RegisterForm):
    """проверка формы при регистрации"""
    all_errors = 0
    if contains_whitespace(form.login.data) is True:
        # пустые символы в логине
        all_errors += 1
        flash('Ошибка: в поле логина не может быть пробелов.', 'error')
    if contains_whitespace(form.email.data) is True:
        # пустые символы в почте
        all_errors += 1
        flash('Ошибка: в поле почты не может быть пробелов.', 'error')
    if len(form.login.data) < 1 or len(form.login.data) > 30:
        # длинна логина
        all_errors += 1
        flash('Ошибка: длина логина не может быть меньше 2 или больше 30 символов.', 'error')
    if '@' not in form.email.data:
        # проверка почты
        all_errors += 1
        flash('Ошибка: неверно указано поле почты (поле должно содержать "@").', 'error')
    all_errors += check_password_form(form.password.data, form.repeated_password.data)
    return int(all_errors)
