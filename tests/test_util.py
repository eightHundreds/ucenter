from unittest import TestCase

from ucenter_api.util import *


class TestUtil(TestCase):
    def test_MD5(self):
        print(Util.MD5('123'))

    def test_ucenter_aucode(self):
        result=Util.ucenter_aucode("12345678910",True)
        print(result)
        pass
