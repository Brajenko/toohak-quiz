import os

from flask import (Flask, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from toohak.forms import *
from toohak.manage_db import *
from toohak.data.users import Anonymous
from toohak.form_examination import *


# CONFIG
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous
app.config['SECRET_KEY'] = '7768efa191c4a3e53bfb5f974c0340c825a9f422c3ea270999f618e2cd9a59df'
global_init('toohak/db/users.db')


# Decorator for checking is quiz running
def check_quiz(handler):
    def better_handler(*args, **kwargs):
        if session.get('is_quiz_going', False) and current_user.is_authenticated:
            return redirect('/quiz')
        return handler(*args, **kwargs)
    better_handler.__name__ = handler.__name__
    return better_handler
    

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


@app.route("/register", methods=["POST", "GET"])
@check_quiz
def register():
    """Register page"""
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


@app.route("/login", methods=["POST", "GET"])
@check_quiz
def login():
    """login page"""
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


@app.route("/account", methods=["POST", "GET"])
@login_required
@check_quiz
def account():
    """account page"""
    return render_template('account.html', title='Аккаунт')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    """for logout"""
    if session.get('is_quiz_going', False):
        end_test_passing()
    logout_user()
    return redirect('/login')


@app.route('/', methods=['GET'])
@check_quiz
def index():
    """index page"""
    return render_template('index.html', quizes=get_all_quizes_for_page(current_user.id))


@app.route('/quiz/start/<int:quiz_id>')
@login_required
@check_quiz
def start_quiz(quiz_id):
    """This function starts quiz and redirect user to the quiz page
    you can't pass your own test"""
    quiz = get_quiz_by_id(quiz_id)
    if quiz.creator == current_user.id:
        return redirect('/')
    
    session['is_quiz_going'] = True
    session['quiz_id'] = quiz_id
    session['questions'] = quiz.get_questions()
    session['curr_question'] = 0
    session['score'] = 0
    return redirect('/quiz')
    

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    """Page for quiz completing
    Checks is answer right, counts user's points"""
    if 'is_quiz_going' not in session or not session['is_quiz_going']:
        #if there is no quizes
        return 'Нет запущенных тестов, запустите новый на <a href="/">Главной странице</a>'
    
    if request.method == 'POST':
        if session['questions'][session['curr_question']]["answer"] == request.form["answer"]:
            session['score'] += 1
        session['curr_question'] += 1
        if session['curr_question'] == len(session['questions']):
            # if quiz ends
            end_test_passing()
            author_id = get_quiz_by_id(session['quiz_id']).user.id
            return render_template('results.html', res=session['score'], quizes=get_all_quizes_for_page(author_id, by_user=True))
        print(session['questions'][session['curr_question']])
        return render_template('quiz.html', question=session['questions'][session['curr_question']], 
                               length=len(session['questions']), curr=session['curr_question'])
    if request.method == 'GET':
        print(session['questions'][session['curr_question']])
        return render_template('quiz.html', question=session['questions'][session['curr_question']], 
                               length=len(session['questions']), curr=session['curr_question'])
        

@app.route('/leaderboard')
@check_quiz
def leaderboard():
    """Leaderboard page"""
    return render_template('leaderboard.html', leaders=get_leaders())


def end_test_passing():
    """function that ends test passing
    setting all vars back to default"""
    session['is_quiz_going'] = False
    max_prev_completion = get_max_completion(current_user.get_id(), session['quiz_id'])
    questions_n = len(session['questions'])
    percents_complete = session['score'] * 100 / questions_n
    add_new_completion(current_user.get_id(), session['quiz_id'], session['score'], percents_complete)
    
    if not max_prev_completion:
        increase = percents_complete * 10
        increase_user_pts(current_user.get_id(), increase)
        return
    
    if max_prev_completion < percents_complete:
        difference = percents_complete - max_prev_completion
        increase = difference * 10
        increase_user_pts(current_user.get_id(), increase)
        return
    

@app.route('/quiz/add', methods=['GET', 'POST'])
@login_required
@check_quiz
def add_quiz():
    """adding quiz page"""
    form = AddQuizForm()
    if form.validate_on_submit():
        add_new_quiz(form, current_user)
        return '''<h1>Тест успешно добавлен!</h1><h3Вы можете><a href="/">перейти на главную<a></h3>'''

    return render_template('add_quiz.html', form=AddQuizForm())


@app.login_manager.unauthorized_handler
def unauth_handler():
    return '''<h1>Для выполнения этого действия нужно <a href="/register">зарегистрироваться</a> или <a href="/login">войти</a></h1>'''