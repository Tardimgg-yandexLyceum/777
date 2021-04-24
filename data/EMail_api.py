import flask
from flask import render_template, make_response, jsonify, request, current_app as app
from flask_mail import Message
import ConfigReader

from CustomClass.AsynsTask import a_sync

blueprint = flask.Blueprint(
    'email_api',
    __name__,

)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@a_sync
def send_async_email(context, mail, msg):
    with context():
        try:
            mail.send(msg)
        except Exception as e:
            print(e)


@blueprint.route(ConfigReader.read_send_password_reset_email(), methods=['POST'])
def send_password_reset_email():
    if not request.json or any(map(lambda x: x not in request.json, ['token', 'recipients'])):
        return jsonify(
            {
                'error': 'no data available'
            }
        )
    token = request.json['token']
    recipients = request.json['recipients']
    msg = Message('[777] Reset Your Password',
                  sender=app.config['ADMINS'][0],
                  recipients=[recipients])
    # msg.body = render_template('forgot_password_message.html',
    #                           token=token)
    msg.body = 'Body of the email to send'
    # msg.html = render_template('forgot_password_message.html', title='Восстановление')
    msg.html = token
    from Main import mail
    send_async_email(app.app_context, mail, msg)
    return jsonify({'success': 'OK'})


@blueprint.route(ConfigReader.read_send_confirmation_email(), methods=['POST'])
def send_confirmation_email():
    if not request.json or any(map(lambda x: x not in request.json, ['token', 'recipients'])):
        return jsonify(
            {
                'error': 'no data available'
            }
        )
    token = request.json['token']
    recipients = request.json['recipients']
    msg = Message('[777] Confirmation Your Email',
                  sender=app.config['ADMINS'][0],
                  recipients=[recipients])
#    msg.body = render_template('email_confirmation_message.txt',
#                               token=token)
    msg.body = 'Body of the email to send'
    msg.html = token
    from Main import mail
    send_async_email(app.app_context, mail, msg)
    return jsonify({'success': 'OK'})

