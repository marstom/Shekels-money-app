from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    full_name = StringField('full_name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])

    def validate(self):
        is_valid = super().validate()
        if self.password.data and self.password2.data:
            if self.password.data != self.password2.data:
                is_valid = False

        return is_valid


class ExpenseForm(FlaskForm):
    _cat_choice=[('a','xbxx'),('a','bsss'),('aaaa','bss')] #teset only
    name = StringField('name', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    category = SelectField(label='Kategoria', choices=[('a','xbxx'),('a','bsss'),('aaaa','bss')])

    def validate(self):
        is_valid = super().validate()

        if self.price.data and self.price.data < 10:
            self.price.errors.append('powyzej 10 musi byc!!!')
            return False

        return is_valid