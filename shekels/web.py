from urllib.parse import urlparse, urljoin

import datetime
from flask import Flask, render_template, request, \
    redirect, url_for, flash, abort, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, \
    login_required, login_user, logout_user, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound

from passlib.hash import pbkdf2_sha256

from shekels.forms import ExpenseForm, LoginForm, RegisterForm

import logging
import shekels.logger

shekels.logger.setup()

app = Flask(__name__)
app.secret_key = 'fdsafhsdalkghsdahg'
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

toolbar = DebugToolbarExtension(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Log in please!"

# SQLite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../expense2.db'

# To change user or password change the postgres:postres part
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://postgres:postgres@localhost/shekels'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    full_name = db.Column(db.String)
    password = db.Column(db.String)
    avatar = db.Column(db.String) #TODO obrazek BASE64

    def __str__(self):
        return "User: {} {}".format(self.login,
                                    self.full_name)

class Expense(db.Model):
    '''
    Each expense is related with user
    '''
    __tablename__ = 'expense'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expense = db.relationship('User', backref='expenses')


class Category(db.Model):
    '''
    Category can have many expenses. one to many
    '''
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    expenses = db.relationship('Expense', backref='category')


class Report(db.Model):
    '''
    Table contains report generated by user
    '''
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)


class PlanndeExpense(db.Model):
    __tablename__ = 'planned_expense'
    id = db.Column(db.Integer, primary_key=True)
    #TODO



def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = db.session.query(User).filter(
                User.login == form.login.data
            ).one()
        except NoResultFound:
            flash(message='bad login')
        else:
            if pbkdf2_sha256.verify(form.password.data, user.password):
                login_user(user)
                flash('Welcome {}!'.format(user.login))
                app.logger.log(10, 'Logged user {}'.format(user.login))
                next = request.args.get('next')
                return redirect(next or url_for('index'))
            else:
                flash(message='bad login')
    return render_template('login.html', form=form)


@app.route('/')
def index():
    logging.info('hello')
    return render_template('index.html')


@app.route('/userlist')
@login_required
def user_list():
    logging.info('DUPA')
    query = db.session.query(User)
    if 'name' in request.args:
        name = '%{}%'.format(request.args['name'])
        query = query.filter(User.name.like(name))

    user_list = query.all()

    return render_template('user_list.html', users=user_list)


@app.route('/expenselist')
@login_required
def list():
    user_id = session['user_id']
    expenses = db.session.query(Expense).filter(Expense.user_id == user_id).all()
    return render_template('list.html',
                           expenses=expenses)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ExpenseForm()
    # form.category.choices=[('kategoria1','dupa')]
    categories = [(cat.id, cat.name) for cat in db.session.query(Category).all()]
    form.category.choices = categories
    if form.validate_on_submit():
        expense = Expense(
            name=form.name.data,
            price=form.price.data
        )
        expense.user_id = session['user_id']
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        secret = pbkdf2_sha256.hash(form.password.data)
        user = User(
            login=form.login.data,
            full_name=form.full_name.data,
            password=secret
        )
        db.session.add(user)
        db.session.commit()
        flash('User registered {}! Please log in.'.format(user.login))
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
