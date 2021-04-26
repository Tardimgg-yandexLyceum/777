import requests
from requests import get, post, delete

import ConfigReader
import get_local_ip

_ip_db = ConfigReader.read_data_base_url()

protocol = ConfigReader.read_web_application_protocol()
host = ConfigReader.read_web_application_host()
if host == 'local':
    host = get_local_ip.get_ip()
port = ConfigReader.read_web_application_port()
if all(map(lambda x: x is not None, [protocol, host, port])):
    _ip_app = f"{protocol}{host}:{port}"
else:
    _ip_app = None


def get_ip_app():
    return _ip_app


def get_bin_user(email: str, user_id=None):
    try:
        if user_id:
            return get(_ip_db + ConfigReader.read_get_bin_user_api_url(), json={
                'id': user_id
            }).json()
        else:
            return get(_ip_db + ConfigReader.read_get_bin_user_api_url(), json={
                'email': email,
            }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def add_user(name: str, surname: str, email: str, hashed_password: str, salt: bytes, confirmed: bool, money: int):
    try:
        return post(_ip_db + ConfigReader.read_users_api_url(), json={
            'email': email,
            "hashed_password": hashed_password,
            'name': name,
            'surname': surname,
            'salt': salt,
            'confirmed': confirmed,
            'money': money
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def get_user(email: str, user_id=None):
    try:
        if user_id:
            return get(_ip_db + ConfigReader.read_user_api_url(), json={
                'id': user_id
            }).json()
        else:
            return get(_ip_db + ConfigReader.read_user_api_url(), json={
                'email': email,
            }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def delete_user(user_id):
    try:
        return delete(_ip_db + ConfigReader.read_users_api_url(), json={
            'id': user_id
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def changing_user_properties(user_id: int, change_properties: dict):
    try:
        return post(_ip_db + ConfigReader.read_user_api_url(), json={
            'id': user_id,
            'change_properties': change_properties
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def check_email(email: str):
    try:
        return get(_ip_db + ConfigReader.read_check_email_api_url(), json={
            'email': email
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def check_id(user_id: int):
    try:
        return get(_ip_db + ConfigReader.read_check_id_api_url(), json={
            'id': user_id
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def add_random_salt_value(value: str):
    try:
        return get(f"{_ip_app}{ConfigReader.read_add_random_salt_value_api_url()}{value}").json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def add_salt_value(value: str, salt: str):
    try:
        return get(_ip_app + ConfigReader.read_add_salt_value_api_url(), json={
            'value': value,
            "salt": salt
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def send_password_reset_email(redirection, recipients):
    try:
        return post(_ip_app + ConfigReader.read_send_password_reset_email_api_url(), json={
            'redirection': redirection,
            "recipients": recipients
        })
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def send_confirmation_email(redirection, recipients):
    try:
        return post(_ip_app + ConfigReader.read_send_confirmation_email_api_url(), json={
            'redirection': redirection,
            "recipients": recipients
        })
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def get_main_events():
    try:
        return get(_ip_app + ConfigReader.read_get_main_events_api_url()).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def get_all_events_by_type(event_type):
    try:
        return get(f"{_ip_app}{ConfigReader.read_get_all_events_by_type_api_url()}{event_type}").json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def get_event(event_type, event):
    try:
        return get(f"{_ip_app}{ConfigReader.read_get_event_api_url()}{event_type}/{event}").json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def read_add_user_event(user_id, money, coef, time):
    try:
        return post(f"{_ip_app}{ConfigReader.read_add_user_event()}", json={
            'money': money,
            'user_id': user_id,
            'coef': coef,
            'time': time
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError
