import flask
from flask import redirect, render_template, make_response, request
from flask_mail import Message
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user, logout_user, current_user

import HomeApi
import Main
from data import ConverterObj, EMail_api
from data.UserController import UserController

blueprint = flask.Blueprint(
    'authorization',
    __name__,

)


class RegistrationForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


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
            user = UserController.UseUserApi.get_bin_user(form.email.data)
            if user:
                if user.confirmed:
                    if user and UserController.check_password(user, form.password.data):
                        login_user(user)
                        return redirect("/")
                else:
                    return render_template('login.html',
                                           message="Подтвердите свой аккаунт",
                                           form=form)
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
            if check_email:
                user_id = UserController.UseUserApi.get_user(form.email.data)['id']
                token = UserController.get_user_token(user_id, 600)
                HomeApi.send_password_reset_email(token, form.email.data)
                return 'Отправлено письмо для восстановления'
            else:
                return render_template('forgot_password.html',
                                       message="Такого пользователя не существует",
                                       form=form)

        except ConnectionError:
            return make_response("Server error", 500)

    return render_template('forgot_password.html', title='Восстановление', form=form)


@blueprint.route('/password_recovery/<token>', methods=['GET', 'POST'])
def password_recovery(token):
    user_id = UserController.verify_user_token(token)
    if not user_id:
        return make_response("Токен недействителен", 403)

    form = PasswordRecoveryForm()
    if form.validate_on_submit():
        try:
            if form.password.data != form.password2.data:
                return render_template("forgot_password.html",
                                       message="Пароли не совпадают",
                                       form=form)
            UserController.changing_user(user_id, {'password': form.password.data})
            return redirect('/login')

        except ConnectionError:
            return make_response("Server error", 500)

    return render_template('forgot_password.html', title='Восстановление', form=form)


@blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            check_email = UserController.UseUserApi.check_email(form.email.data)
            if not check_email:
                UserController.create_user(email=form.email.data, password=form.password.data,
                                           name=form.name.data, surname=form.surname.data, confirmed=False)
                token = UserController.get_user_token(form.email.data, 600)
                HomeApi.send_confirmation_email(token, form.email.data)
                return 'Отправлено письмо для подтверждения'
            elif not UserController.UseUserApi.get_user(form.email.data)['confirmed']:
                user_id = UserController.UseUserApi.get_user(form.email.data)['id']
                UserController.UseUserApi.delete_user(user_id)

                UserController.create_user(email=form.email.data, password=form.password.data,
                                           name=form.name.data, surname=form.surname.data, confirmed=False)
                token = UserController.get_user_token(form.email.data, 600)
                HomeApi.send_confirmation_email(token, form.email.data)
                return 'Отправлено письмо для подтверждения'
            else:
                return render_template('registration.html',
                                       message="Такой пользователь уже существует",
                                       form=form)
        except ConnectionError:
            return make_response("Server error", 500)

    return render_template('registration.html', title='Регистрация', form=form)


@blueprint.route('/confirmation_email/<token>', methods=['GET', 'POST'])
def confirmation_email(token):
    email = UserController.verify_user_token(token)
    if not email:
        return make_response("Токен недействителен", 403)

    if UserController.UseUserApi.check_email(email):
        user_id = UserController.UseUserApi.get_user(email=email)['id']
        UserController.changing_user(user_id, {'confirmed': True})
        return redirect("/login")
    else:
        return make_response("Токен недействителен", 403)
