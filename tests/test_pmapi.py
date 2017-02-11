# -*- coding: utf-8 -*-
import json
import unittest
from unittest import TestCase

import xmltodict

from ucenter_api.clients import PmApi
from tests import TEST_USERNAME, TEST_PSW, TEST_EMAIL

class TestUserapi(TestCase):
    def setUp(self):
        self.api=PmApi()
    def test_send(self):
        result=self.api.uc_pm_sendpm('1','2','测试','测试')
        self.assertGreater(int(result),0)
    def test_list(self):
        result=self.api.uc_pm_ls('2')
        self.assertIsNotNone(result)