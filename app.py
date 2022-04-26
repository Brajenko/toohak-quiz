from flask import (Flask, flash, make_response, redirect, render_template,
                   request, session, url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from forms import *
from manage_db import *
from data.users import Anonymous

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous
app.config['SECRET_KEY'] = 'ULTRAMEGASECRETKEY'


def check_quiz(handler):
    def better_handler(*args, **kwargs):
        if session.get('is_quiz_going', False):
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
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.data)
        add_new_user(form)
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация')


@app.route("/login", methods=["POST", "GET"])
@check_quiz
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(get_user_by_email(form.email.data), remember=True)
        return redirect('/')
        # if form.email.data != 'saq':
        #     flash('AAAAAA', 'error')
    return render_template('login_form.html', form=form, title='Логин')    


@app.route("/account", methods=["POST", "GET"])
@login_required
@check_quiz
def account():
    return render_template('account.html', title='Аккаунт')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if session.get('is_quiz_going', False):
        end_test_passing()
    logout_user()
    return redirect('/login')


@app.route('/', methods=['GET'])
@check_quiz
def index():
    return render_template('index.html', quizes=get_all_quizes_for_page(current_user.id))


@app.route('/quiz/start/<int:quiz_id>')
@login_required
@check_quiz
def start_quiz(quiz_id):
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
    if 'is_quiz_going' not in session or not session['is_quiz_going']:
        return 'Нет запущенных тестов, запустите новый на <a href="/">Главной странице</a>'
    
    if request.method == 'POST':
        if session['questions'][session['curr_question']]["answer"] == request.form["answer"]:
            session['score'] += 1
        session['curr_question'] += 1
        if session['curr_question'] == len(session['questions']):
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
    return render_template('leaderboard.html', leaders=get_leaders())


def end_test_passing():
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
    form = AddQuizForm()
    if form.validate_on_submit():
        add_new_quiz(form, current_user)
        return '''<h1>Тест успешно добавлен!</h1><h3Вы можете><a href="/">перейти на главную<a></h3>'''

    return render_template('add_quiz.html', form=AddQuizForm())


@app.login_manager.unauthorized_handler
def unauth_handler():
    return '''<h1>Для выполнения этого действия нужно <a href="/register">зарегистрироваться</a> или <a href="/login">войти</a></h1>'''



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
