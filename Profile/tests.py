# coding=utf-8
import datetime

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from .models import UserProfile
# Create your tests here.


class UserProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="some_user")

    """测试profile是否被成功创建"""

    def test_profile_auto_create(self):
        self.assertIsNotNone(self.user.profile)

    """测试年龄系统"""

    def test_ages(self):
        self.user.profile.birthDate = (timezone.now()-datetime.timedelta(days=365)).date()
        self.assertEqual(self.user.profile.age, 1)

    def test_default_birth(self):
        """测试在没有设置生日的时候的默认年龄"""
        self.assertEqual(self.user.profile.age, 45)

    """测试认证"""

    def test_identification(self):
        self.user.profile.identified = True
        self.user.save()
        self.assertIsNotNone(self.user.profile.identified_date)