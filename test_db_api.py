import codecs
import pickle
import unittest

from requests import get
from data import ConverterObj
import HomeApi


class TestDBApi(unittest.TestCase):
    def setUp(self) -> None:
        self.email = 'qwe@qwe'
        pass

    def test_api_get_non_existent_email(self):
        response_json = HomeApi.check_email("123")
        self.assertEqual('error' in response_json, False)

    def test_api_check_email(self):
        response_json = HomeApi.check_email(self.email)
        self.assertEqual(response_json['contains_value'], True)

    def test_api_get_non_existent_bin_user(self):
        response_json = HomeApi.get_bin_user("123")
        self.assertEqual('message' in response_json and 'not found' in response_json["message"], True)

    def test_api_get_bin_user(self):
        bin_user = HomeApi.get_bin_user(self.email)
        user = ConverterObj.decode(bin_user)

        self.assertEqual(user.email, self.email)

    def test_api_get_user(self):
        user = HomeApi.get_user(self.email)
        self.assertEqual(type(user), dict)
        self.assertEqual(user['email'], self.email)

    def test_api_get_non_existent_user(self):
        response_json = HomeApi.get_user("123")
        self.assertEqual('message' in response_json and 'not found' in response_json["message"], True)

    def tearDown(self) -> None:
        pass
