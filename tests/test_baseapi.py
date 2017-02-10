import unittest
from unittest import TestCase
from api import *
import xmltodict
import  json

class TestBaseapi(TestCase):
    def setUp(self):
        self.api=baseapi()
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