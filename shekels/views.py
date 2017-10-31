from urllib.parse import urlparse, urljoin
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, login_user, logout_user, LoginManager
from sqlalchemy.orm.exc import NoResultFound
from passlib.hash import pbkdf2_sha256

from shekels.app import app
from shekels.forms import ExpenseForm, LoginForm, RegisterForm, EditCategoryForm
from shekels.models import User, Category, Expense, db

import logging

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Log in please!"


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
def expense_list():
    user_id = session['user_id']
    expenses = db.session.query(Expense).filter(Expense.user_id == user_id).all()
    suma=0
    for el in expenses:
        logging.info('price = {} {}'.format(el.price, el.user_id))
        suma+=el.price
    return render_template('expense_list.html',
                           expenses=expenses,
                           suma_wydatkow=suma)


@app.route('/addexpense', methods=['GET', 'POST'])
@login_required
def add():
    form = ExpenseForm()
    categories = [(cat.id, cat.name) for cat in db.session.query(Category).filter(Category.user_id == session['user_id']).all()]
    form.category.choices = categories
    vak = form.validate()
    if request.method == 'POST' and form.validate():
        expense = Expense(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            category_id=int(form.category.data), #data?
            user_id = session['user_id'],
        )
        # expense.user_id = session['user_id']
        logging.warning('user id {} catuserid {}'.format(session['user_id'], expense.category_id))
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('index'))
    flash(form.errors)

    return render_template('add_expense.html', form=form)


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

@app.route('/editcategories', methods=['GET', 'POST'])
@login_required
def edit_categories():
    form = EditCategoryForm()
    category = Category(
        name=form.name.data,
        description=form.description.data,
        user_id=session['user_id'],
    )
    db.session.add(category)
    db.session.commit()

    if request.method == 'POST':
        if request.form['btn'] == 'delete_category':
            category_id = request.form['category']
            print(category_id)
            query = db.session.query(Category).filter(Category.id == category_id).delete()
            db.session.commit()
            print(request.form)

    categories = db.session.query(Category).filter(Category.user_id == session['user_id'])

    return render_template('edit_categories.html', form=form, categories=categories)

@app.route("/testpage")
def testpage():
    categ = db.session.query(Category.expenses).all()
    #filter only items that belongs to cat 1
    items = db.session.query(Expense).filter(Expense.category_id == 1 and Expense.user_id == 1).all()
    # logging.warning('to.... {}'.format(items))
    asdf = session
    return render_template('test_page.html', categ=categ, items=items)

if __name__ == '__main__':
    app.run(debug=True)

