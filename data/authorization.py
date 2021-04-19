import flask
from flask import redirect, render_template, make_response
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user, logout_user

import HomeApi
from data import ConverterObj
from data.UserController import UserController

blueprint = flask.Blueprint(
    'authorization',
    __name__,

)


class RegistrationForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('&#xf0da;')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user_bin = HomeApi.get_bin_user(form.email.data)
            if type(user_bin) is str:
                user = ConverterObj.decode(user_bin)
                if user and UserController.check_password(user, form.password.data):
                    login_user(user)
                    return redirect("/main")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        except ConnectionError:
            return make_response("Server error", 500)

    return render_template('login.html', title='Авторизация', form=form)


@blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user_bin = HomeApi.get_bin_user(form.email.data)
            if type(user_bin) is str:
                user = ConverterObj.decode(user_bin)
                if user and UserController.check_password(user, form.password.data):
                    login_user(user)
                    return redirect("/main")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        except ConnectionError:
            return make_response("Server error", 500)

    return render_template('login.html', title='Авторизация', form=form)


@blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user_bin = HomeApi.get_bin_user(form.email.data)
            if type(user_bin) is str:
                user = ConverterObj.decode(user_bin)
                if user and UserController.check_password(user, form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    return redirect("/main")
            return render_template('registration.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        except ConnectionError:
            return make_response("Server error", 500)

    return render_template('registration.html', title='Регистрация', form=form)
