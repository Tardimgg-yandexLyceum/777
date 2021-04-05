import requests
from requests import get
import configparser

import ConfigReader

_ip_db = ConfigReader.readDataBaseUrl()


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
