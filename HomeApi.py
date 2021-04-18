import requests
from requests import get
import configparser

import ConfigReader
import get_local_ip

_ip_db = ConfigReader.readDataBaseUrl()

protocol = ConfigReader.readWebApplicationProtocol()
host = ConfigReader.readWebApplicationHost()
if host == 'local':
    host = get_local_ip.get_ip()
port = ConfigReader.readWebApplicationPort()
if all(map(lambda x: x is not None, [protocol, host, port])):
    _ip_app = f"{protocol}{host}:{port}"
else:
    _ip_app = None


def get_user_old(email: str):
    try:
        return get(_ip_db + "/api/get_user", json={
            'email': email
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def get_bin_user(email: str):
    try:
        return get(_ip_db + "/api/user", json={
            'email': email
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def get_user(email: str):
    try:
        return get(_ip_db + "/api/userProperties", json={
            'email': email
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def check_email(email: str):
    try:
        return get(_ip_db + "/api/check_email", json={
            'email': email
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def add_random_salt_value(value: str):
    try:
        return get(f"{_ip_app}/api/addRandomSalt/{value}").json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError


def add_salt_value(value: str, salt: str):
    try:
        return get(_ip_app + "/api/addSalt", json={
            'value': value,
            "salt": salt
        }).json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError
