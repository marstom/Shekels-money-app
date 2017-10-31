import datetime

from flask_login import UserMixin
from shekels.db_sqlalchemy import db

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
    price = db.Column(db.Float)
    description = db.Column(db.String)
    date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='expenses')
    cat=db.relationship('Category', backref='expense')

class Category(db.Model):
    '''
    Category can have many expenses. one to many
    '''
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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

