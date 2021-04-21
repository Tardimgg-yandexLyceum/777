import codecs
import pickle
import unittest

from requests import get

import ConfigReader
import get_local_ip
from data import ConverterObj
import HomeApi


class TestDBApi(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_api_random_salt_value(self):
        host_web_app = ConfigReader.read_web_application_host()
        port_web_app = int(ConfigReader.read_web_application_port())
        if host_web_app == "local":
            start_url = f"{ConfigReader.read_web_application_protocol()}{get_local_ip.get_ip()}:{port_web_app}"
        else:
            start_url = f"{ConfigReader.read_web_application_protocol()}{host_web_app}:{port_web_app}"
        response_json = get(start_url + '/api/addRandomSalt/qwe').json()
        self.assertEqual('salt' in response_json, True)
        self.assertEqual('salt_value' in response_json, True)

    def test_api_random_salt_non_value(self):
        host_web_app = ConfigReader.read_web_application_host()
        port_web_app = int(ConfigReader.read_web_application_port())
        if host_web_app == "local":
            start_url = f"{ConfigReader.read_web_application_protocol()}{get_local_ip.get_ip()}:{port_web_app}"
        else:
            start_url = f"{ConfigReader.read_web_application_protocol()}{host_web_app}:{port_web_app}"
        response_json = get(start_url + '/api/addRandomSalt/')
        self.assertEqual(response_json.status_code == 404, True)

    def test_api_with_salt_value(self):
        host_web_app = ConfigReader.read_web_application_host()
        port_web_app = int(ConfigReader.read_web_application_port())
        if host_web_app == "local":
            start_url = f"{ConfigReader.read_web_application_protocol()}{get_local_ip.get_ip()}:{port_web_app}"
        else:
            start_url = f"{ConfigReader.read_web_application_protocol()}{host_web_app}:{port_web_app}"

        response_salt_value_json = get(start_url + '/api/addRandomSalt/qwe').json()

        self.assertEqual('salt' in response_salt_value_json, True)
        self.assertEqual('salt_value' in response_salt_value_json, True)

        response_with_salt_json = get(start_url + '/api/addSalt', json={
            'value': 'qwe',
            'salt': response_salt_value_json["salt"]
        }).json()

        self.assertEqual('salt' in response_with_salt_json, True)
        self.assertEqual('salt_value' in response_with_salt_json, True)

        self.assertEqual(response_with_salt_json['salt'] == response_salt_value_json['salt'], True)
        self.assertEqual(response_with_salt_json['salt_value'] == response_salt_value_json['salt_value'], True)

    def tearDown(self) -> None:
        pass
