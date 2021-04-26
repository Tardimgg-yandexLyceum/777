import random
from random import choice
from time import time

import flask
from flask import jsonify, make_response

import ConfigReader

blueprint = flask.Blueprint(
    'event_api',
    __name__,

)

events = []

football_clubs = ["Ювентус", "Барселона", "Зенит", "Локомотив", "Челси", "Арсенал", "Милан", "Реал-Мадрид", "Боруссия",
                  "Салют"]
volleyball_clubs = ["Белогорье", "Зенит-Казань", "Динамо", "Автомобилист", "Обнинск", "Шахтер", "Экран", "Луч",
                    "Воронеж", "Кузбасс"]
hockey_clubs = ["Авангард", "Трактор", "Локомотив", "Металлург-Мг", "Ак-Барс", "СКА", "Буран", "Гаага", "Барыс",
                "Галкан"]
basketball_clubs = ["ЦСКА", "Енисей", "Химки", "Парма", "Зенит", "УГМК", "Локомотив-Кубань", "Юта-Джаз", "УНИКС",
                    "Русичи"]


def clear_event():
    delete = []
    for i in range(len(events)):
        if events[i]['time'] <= time():
            delete.append(i)
    for index in delete[::-1]:
        del events[index]


def create_event():
    for sport in [['football', football_clubs], ['volleyball', volleyball_clubs], ['hockey', hockey_clubs],
                  ['basketball', basketball_clubs]]:
        for _ in range(5):
            events.append({
                'sport': sport[0],
                'team_1': choice(sport[1]),
                'team_2': choice(sport[1]),
                'coef': [random.uniform(1, 3) for _ in range(9)],
                'time': time() + random.randint(30, 600)
            })


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.route(f"{ConfigReader.read_get_event_api_url()}/<string:event_type>/<string:event>", methods=['GET'])
def get_event(event_type, event):
    translate = {
        "футбол": "football",
        "волейбол": "volleyball",
        "хоккей": "hockey",
        "баскетбол": "basketball"
    }
    event_type = translate[event_type.lower()]

    answer = {
        "columns": ['Команды', 'Победа 1', 'Победа 2', '1:0', "2:0", "2:1", "2:2", "0:1", "0:2", "1:2"],
    }

    for value in events:
        if value['sport'] == event_type and f"{value['team_1']}_{value['team_2']}" == event or \
                f"{value['team_2']}_{value['team_1']}" == event:
            answer['1'] = value.copy()
            break
    return jsonify(answer)


@blueprint.route(f"{ConfigReader.read_get_all_events_by_type_api_url()}/<string:event_type>", methods=['GET'])
def get_all_events_by_type(event_type):
    clear_event()

    if len(events) <= 20:
        create_event()

    translate = {
        "футбол": "football",
        "волейбол": "volleyball",
        "хоккей": "hockey",
        "баскетбол": "basketball"
    }
    event_type = translate[event_type.lower()]

    answer = {
        "columns": ['Команды', 'Победа 1', 'Победа 2', '1:0', "2:0", "2:1", "2:2", "0:1", "0:2", "1:2"],
    }

    i = 1
    for value in events:
        if value['sport'] == event_type:
            answer[str(i)] = value.copy()
            i += 1

    return jsonify(answer)


@blueprint.route(ConfigReader.read_get_main_events_api_url(), methods=['GET'])
def get_main_events():
    clear_event()

    if len(events) <= 20:
        create_event()

    translate = {
        "football": "Футбол",
        "volleyball": "Волейбол",
        "hockey": "Хоккей",
        "basketball": "Баскетбол",
    }
    answer = {
        'Футбол': {
            'short_info': "Ставки на футбол",
            'first_event': "",
            'second_event': "",
            'third_event': ""
        },

        'Волейбол': {
            'short_info': "Ставки на волейбол",
            'first_event': "",
            'second_event': "",
            'third_event': ""
        },
        'Хоккей': {
            'short_info': "Ставки на хоккей",
            'first_event': "",
            'second_event': "",
            'third_event': ""
        },

        'Баскетбол': {
            'short_info': "Ставки на баскетбол",
            'first_event': "",
            'second_event': "",
            'third_event': ""
        }
    }
    for event in events:
        if not answer[translate[event['sport']]]['first_event']:
            answer[translate[event['sport']]]['first_event'] = f"{event['team_1']} vs {event['team_2']}"

        elif not answer[translate[event['sport']]]['second_event']:
            answer[translate[event['sport']]]['second_event'] = f"{event['team_1']} vs {event['team_2']}"

        elif not answer[translate[event['sport']]]['third_event']:
            answer[translate[event['sport']]]['third_event'] = f"{event['team_1']} vs {event['team_2']}"

    return jsonify(
        answer
    )
