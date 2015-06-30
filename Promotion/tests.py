# coding=utf-8
from django.test import TestCase

from django.contrib.auth import get_user_model

from .models import Share, ShareRecord
# Create your tests here.


class ShareTest(TestCase):

    def setUp(self):
        self.user = get_user_model().object.create(username="")

    """测试分享链接生成"""

    def test_share_creation(self):
        pass

    def test_get_share_line(self):
        pass


class ShareRecordTest(TestCase):

    def setUp(self):
        pass

    """测试用户通过分享链接进入的行为"""

    def test_respond_to_share(self):
        pass

    def test_respond_to_share_twice(self):
        pass