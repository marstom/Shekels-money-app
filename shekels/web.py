from urllib.parse import urlparse, urljoin

import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_required, login_user, logout_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exists
from werkzeug.exceptions import abort

from shekels.db import DB, User, Expense
from shekels.forms import ExpenseForm, LoginForm, RegisterForm

import logging
import shekels.logger
shekels.logger.setup()

app = Flask(__name__)
app.secret_key = 'fdsafhsdalkghsdahg'
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Zarejestruj się zanim użyjesz aplikacji!"

db = DB('expenses.db')
db.create_db()
session = db.get_session()


logging.getLogger('werkzeug').setLevel(logging.ERROR) # w ten sposób wyciszyliśmy loggera werkzeug

#wzięte ze snippetów
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@login_manager.user_loader
def load_user(id):
    return session.query(User).get(id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = session.query(User).filter(
                User.login == form.login.data
            ).one()
        except NoResultFound:
            flash(message='bad login')
        else:
            if user.password == form.password.data:
                login_user(user)
                flash('Welcome {}!'.format(user.login))
                logging.warning('Logged user {}'.format(user.login))

                next = flask.request.args.get('next')
                if not is_safe_url(next):
                    return abort(400)

                return redirect(next or url_for('index')) #dodać next
            else:
                # app.logger.log(10, 'User wrong login or password user:{}, pass:{}'.format(form.login.data, form.password.data))
                logging.warning('User wrong login or password user:{}, pass:{}'.format(form.login.data, form.password.data))
                flash(message='bad login')
    return render_template('login.html', form=form)


@app.route('/')
def index():
    app.logger.log(10, 'User logged to index page')
    return render_template('index.html')


@app.route('/userlist')
@login_required
def user_list():
    query = session.query(User)
    if 'name' in request.args:
        name = '%{}%'.format(request.args['name'])
        query = query.filter(User.name.like(name))

    user_list = query.all()
    return render_template('user_list.html', users=user_list)


@app.route('/expenselist')
@login_required
def list():
    expenses = session.query(Expense).all()
    return render_template('list.html',
                           expenses=expenses)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            name=form.name.data,
            price=form.price.data
        )
        session = db.get_session()
        session.add(expense)
        session.commit()
        return redirect(url_for('index'))

    return render_template('add.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db.get_session()
        exist = session.query(exists().where(User.login == form.login.data)).scalar()
        if exist:
            flash(message='Taki użytkownik już istnieje. Wpisz inną nazwę')
            return render_template('register.html', form=form)
        user = User(login=form.login.data, full_name=form.full_name.data, password=form.password.data)
        session.add(user)
        session.commit()
        flash('User registered {}! Please log in.'.format(user.login))
        return redirect(url_for('index'))

    else:
        # app.logger.log(10, 'User not register!!! Failed username:{} password:{}'.format(form.login.data, form.password.data))
        logging.error('User not register!!! Failed username:{} password:{}'.format(form.login.data, form.password.data))
        flash(message='Hasła są niezgodne! Wpisz jeszcz raz/')

    return render_template('register.html', form=form)


@app.route('/logoout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()



