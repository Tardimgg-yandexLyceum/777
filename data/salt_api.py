import flask
from flask import jsonify, make_response, request
import os

blueprint = flask.Blueprint(
    'salt_api',
    __name__,

)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.route('/api/addRandomSalt/<string:value>', methods=['GET'])
def add_random_salt_value(value: str):
    additional_salt = os.urandom(50)
    if len(value) >= len(additional_salt):
        salt_value = value + "".join(list(map(chr, additional_salt)))
    else:
        salt_value = []
        for i in range(len(value)):
            salt_value.append(chr(ord(value[i]) ^ additional_salt[i]))

        salt_value.extend(map(chr, additional_salt[len(value)::]))
        salt_value = "".join(salt_value)

    return jsonify(
        {
            'salt': list(additional_salt),
            "salt_value": salt_value
        }
    )


@blueprint.route('/api/addSalt', methods=['GET'])
def add_salt_value():
    if not request.json or any(map(lambda x: x not in request.json, ['value', 'salt'])):
        return jsonify(
            {
                'error': 'no data available'
            }
        )
    additional_salt = request.json['salt']
    value = request.json['value']
    if len(value) >= len(additional_salt):
        salt_value = value + "".join(map(lambda x: chr(x), list(additional_salt)))
    else:
        salt_value = []
        for i in range(len(value)):
            salt_value.append(chr(ord(value[i]) ^ int(additional_salt[i])))
        salt_value.extend(map(chr, additional_salt[len(value)::]))
        salt_value = "".join(salt_value)

    return jsonify(
        {
            'salt': list(additional_salt),
            "salt_value": salt_value
        }
    )
