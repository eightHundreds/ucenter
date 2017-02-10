import unittest
from unittest import TestCase
from api import *
import xmltodict
import  json

TEST_USERNAME='bbdbbbbp'
TEST_PSW='123456'
TEST_EMAIL='1@qq.com'

class TestUserapi(TestCase):
    def setUp(self):
        self.api=userapi()
    @unittest.skip('用户注册,用过一次除非参数修改不能再用了')
    def test_uc_user_register(self):
        result=self.api.uc_user_register(TEST_USERNAME,TEST_PSW,TEST_EMAIL)
        print(result)

    def test_get_user(self):
        r=self.api.uc_get_user(TEST_USERNAME)
        print(json.dumps(xmltodict.parse(r)["root"]))

    def test_user_login(self):
        result=self.api.uc_user_login(TEST_USERNAME,TEST_PSW)
        pass

