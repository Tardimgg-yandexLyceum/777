import flask
from flask import jsonify, make_response

blueprint = flask.Blueprint(
    'salt_api',
    __name__,

)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.route('/api/salt/<string:value>', methods=['GET'])
def add_salt_value(value: str):
    salt_value = value
    return jsonify(
        {
            'salt_value': salt_value
        }
    )

