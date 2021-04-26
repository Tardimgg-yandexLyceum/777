from math import floor
from random import choice
from time import time, sleep

import flask
from flask import request, jsonify

import ConfigReader
from data.UserController import UserController

blueprint = flask.Blueprint(
    'event_api_server',
    __name__,

)

events = []


@blueprint.route(ConfigReader.read_add_user_event(), methods=['POST'])
def add_user():
    if not request.json or any(map(lambda x: x not in request.json, ['user_id', 'coef', "time", 'money'])):
        return jsonify(
            {
                'error': 'no data available'
            }
        )
    events.append({
        "user_id": request.json['user_id'],
        'coef': request.json['coef'],
        'time': request.json['time'],
        'money': request.json['money']
    })
    return jsonify({'success': 'OK'})


def event_service():
    while True:
        delete = []
        sleep(10)
        for i in range(len(events)):
            user = events[i]
            if time() >= user['time']:
                is_win = choice([False, True])
                if is_win:
                    last_money = UserController.UseUserApi.get_user(email='', user_id=user['user_id'])['money']
                    UserController.changing_user(user['user_id'], {
                        'money': floor(last_money + (float(user['coef']) * int(user['money'])))
                    })
                delete.append(i)
        for index in delete[::-1]:
            del events[index]
