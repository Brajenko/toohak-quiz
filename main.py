from flask import (Flask, flash, make_response, redirect, render_template,
                   request, session, url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from forms import *
from manage_db import *
from data.users import Anonymous
from form_examination import *

app = Flask(__name__)
# bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'ULTRAMEGASECRETKEY'


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = get_user_by_login(form.login.data)
        if get_user_by_login(form.login.data):
            if user.check_password(form.password.data):
                login_user(get_user_by_login(form.login.data))
                return redirect(url_for('account'))
            else:
                flash('Ошибка: неверный пароль.', 'error')
        else:
            flash('Ошибка: неверная пара логин пароль.', 'error')
    return render_template('login_form.html', form=form, title='Логин')


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        try:
            if check_form(form) == 0:
                add_new_user(form)
                flash('Успещная регистрация!', 'success')
                return redirect(url_for('login'))
        except:
            flash('Ошибка: на данный login уже зарегестрирован пользователь.', 'error')
    return render_template('register.html', form=form, title='Регистрация')


@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    return render_template('account.html', title='Аккаунт')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
