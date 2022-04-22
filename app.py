from flask import Flask, make_response, redirect, render_template, request, session, flash, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from manage_db import (add_new_quiz, add_new_user, get_quiz_by_id,
                       get_user_by_id)
from forms import *


app = Flask(__name__)
# bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'ULTRAMEGASECRETKEY'


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        add_new_user(form)
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация')


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data != 'saq':
            flash('AAAAAA', 'error')
    return render_template('login_form.html', form=form, title='Логин')    


@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    return render_template('account.html', title='Аккаунт')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@login_required
@app.route('/quiz/start/<int:quiz_id>')
def start_quiz(quiz_id):
    session['is_quiz_going'] = True
    session['questions'] = get_quiz_by_id(quiz_id).get_questions()
    print(session['questions'])
    session['curr_question'] = 0
    session['score'] = 0
    return redirect('/quiz')
    

@login_required
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'is_quiz_going' not in session or session['is_quiz_going'] == False:
        return 'Вы уже прошли тест, запустите новый на <a href="/">Главной странице</a>'
    
    if request.method == 'POST':
        if session['questions'][session['curr_question']]["answer"] == request.form["answer"]:
            session['score'] += 1
        session['curr_question'] += 1
        if session['curr_question'] == len(session['questions']):
            end_test_passing()
            return render_template('results.html', res=session['score'])
        return render_template('quiz.html', question=session['questions'][session['curr_question']])
    if request.method == 'GET':
        print(session['questions'][session['curr_question']])
        return render_template('quiz.html', question=session['questions'][session['curr_question']])


def end_test_passing():
    session['is_quiz_going'] = False


# @login_required
@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    form = AddQuizForm()
    if form.validate_on_submit():
        add_new_quiz(form, current_user)
        return 'тест добавлен'

    return render_template('add_quiz.html', form=AddQuizForm())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
