import flask
from flask import jsonify, make_response
import os

blueprint = flask.Blueprint(
    'salt_api',
    __name__,

)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.route('/api/salt/<string:password>', methods=['GET'])
def add_salt_value(password: str):
    additional_salt = os.urandom(50)
    if len(password) >= 50:
        salt_value = password + "".join(list(map(chr, additional_salt)))
    else:
        salt_value = []
        for i in range(len(password)):
            salt_value.append(chr(ord(password[i]) ^ additional_salt[i]))
        salt_value.extend(map(str, additional_salt[len(password)::]))
        salt_value = "".join(salt_value)

    return jsonify(
        {
            'salt': list(additional_salt),
            "salt_value": salt_value
        }
    )

