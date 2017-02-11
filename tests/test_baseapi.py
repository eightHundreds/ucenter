import  json
from unittest import TestCase

import xmltodict

from ucenter_api.clients import *


class TestBaseapi(TestCase):
    def setUp(self):
        self.api=BaseApi()
    def test_post(self):
        result=self.api.post('app','ls')
        print(json.dumps( xmltodict.parse(result)["root"]))
        print(result)
    def test_module_not_found(self):
        with self.assertRaises(UcenterError) as e:
            self.api.post('user1','abc')
        self.assertEqual(e.exception.msg,'Module not found!')
    def test_action_not_found(self):
        with self.assertRaises(UcenterError) as e:
            self.api.post('user','abc')
        self.assertEqual(e.exception.msg,'Action not found!')