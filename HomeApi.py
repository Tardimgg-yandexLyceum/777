import requests
from requests import get, post
import configparser

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


def get_bin_user(email: str):
    try:
        return get(_ip_db + ConfigReader.read_get_bin_user_api_url(), json={
            'email': email
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def add_user(name: str, surname: str, age: int, email: str, hashed_password: str, salt: bytes):
    try:
        return post(_ip_db + ConfigReader.read_add_user_api_url(), json={
            'email': email,
            "hashed_password": hashed_password,
            'name': name,
            'surname': surname,
            'age': age,
            'salt': salt,
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def get_user(email: str):
    try:
        return get(_ip_db + ConfigReader.read_get_user_api_url(), json={
            'email': email
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
