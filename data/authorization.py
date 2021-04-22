import flask
from flask import redirect, render_template, make_response, request
from flask_mail import Message
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user, logout_user

import HomeApi
import Main
from data import ConverterObj, EMail_api
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
    submit = SubmitField()


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Отправить письмо')


class PasswordRecoveryForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user_bin = UserController.UseUserApi.get_bin_user(form.email.data)
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
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        try:
            check_email = UserController.UseUserApi.check_email(form.email.data)
            if check_email['contains_value']:
                user_id = UserController.UseUserApi.get_user(form.email.data)['id']
                token = UserController.get_reset_password_token(user_id, 600)
                HomeApi.send_password_reset_email(token, form.email.data)
                return 'Mail Sent...'
            else:
                return render_template('forgot_password.html',
                                       message="Такого пользователя не существует",
                                       form=form)

        except ConnectionError:
            return make_response("Server error", 500)

    return render_template('forgot_password.html', title='Восстановление', form=form)


@blueprint.route('/password_recovery/<token>', methods=['GET', 'POST'])
def password_recovery(token):
    user_id = UserController.verify_reset_password_token(token)
    if not user_id:
        return make_response("Токен недействителен", 403)

    form = PasswordRecoveryForm()
    if form.validate_on_submit():
        try:
            if form.password.data != form.password2.data:
                return render_template("forgot_password.html",
                                       message="Пароли не совпадают",
                                       form=form)
            HomeApi.changing_user_properties(user_id, {'password': form.password.data})
            return "Пароль изменен"

        except ConnectionError:
            return make_response("Server error", 500)

    return render_template('forgot_password.html', title='Восстановление', form=form)


@blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            check_email = UserController.UseUserApi.check_email(form.email.data)
            if not check_email['contains_value']:
                UserController.create_user(email=form.email.data, password=form.password.data,
                                           name='qwe', surname='qwe', age=18)
            else:
                return render_template('registration.html',
                                       message="Такой пользователь уже существует",
                                       form=form)
            # user_bin = HomeApi.get_bin_user(form.email.data)
            # if type(user_bin) is str:
            #    user = ConverterObj.decode(user_bin)
            #    if user and UserController.check_password(user, form.password.data):
            #        login_user(user, remember=form.remember_me.data)
            #        return redirect("/main")
            # return render_template('registration(old).html',
            #                       message="Неправильный логин или пароль",
            #                       form=form)
        except ConnectionError:
            return make_response("Server error", 500)

    return render_template('registration.html', title='Регистрация', form=form)
