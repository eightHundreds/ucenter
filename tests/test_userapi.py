import json
import unittest
from unittest import TestCase

import xmltodict

from tests import TEST_USERNAME, TEST_PSW, TEST_EMAIL
from ucenter_api.clients import *


class TestUserapi(TestCase):
    def setUp(self):
        self.api = userapi()

    # @unittest.skip('用户注册,用过一次除非参数修改不能再用了')
    def test_uc_user_register(self):
        result = self.api.uc_user_register(TEST_USERNAME, TEST_PSW, TEST_EMAIL)
        print(result)

    def test_get_user(self):
        r = self.api.uc_get_user(TEST_USERNAME)
        self.assertIsNotNone(r)
        print(r)

    def test_user_login(self):
        result = self.api.uc_user_login(TEST_USERNAME, TEST_PSW)
        pass

    def test_uc_user_login(self):
        result = self.api.uc_user_login(TEST_USERNAME, TEST_PSW)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], UserLoginResult.Success)
        self.assertEqual(result[1].get('username'), TEST_USERNAME)

        result = self.api.uc_user_login(666, TEST_PSW)
        self.assertEqual(result[0], UserLoginResult.NotExist)

        result = self.api.uc_user_login(TEST_USERNAME, 666)
        self.assertEqual(result[0], UserLoginResult.PassWordError)

    def test_uc_user_synlogin(self):
        result=self.api.uc_user_synlogin(1)
        self.assertIsNotNone(result)
        self.assertGreater(len(result),0)
    def test_uc_user_synlogout(self):
        result=self.api.uc_user_synlogout()
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
    def test_uc_user_checkemail(self):
        result=self.api.uc_user_checkemail(TEST_EMAIL)
        self.assertIsNotNone(result)
        self.assertEqual(result,UserEmailCheckResult.EmailHasBeenRegistered)
