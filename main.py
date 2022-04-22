from flask import Flask, render_template, request, url_for, redirect, flash
from forms import LoginForm, RegisterForm
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)
from flask_bcrypt import Bcrypt

from manage_db import (add_new_quiz, add_new_user, get_quiz_by_id, get_user_by_id)

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'lol'


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


@app.route("/login", methods=["POST", "GET"])
def login():
    # Логирование - пробный вариант
    form = LoginForm()
    if form.validate_on_submit():
        # test
        if form.email.data != 'saq':
            # test
            flash('AAAAAA', 'error')
    return render_template('login_form.html', form=form, title='Логин')


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # test
        add_new_user(form)
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация')


@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    return render_template('account.html', title='Аккаунт')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
