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
        self.user.profile = UserProfile.objects.get_or_create(user=self.user)[0]

    def test_profile_auto_create(self):
        self.assertIsNotNone(self.user.profile)

    def test_ages(self):
        self.user.profile.birthDate = (timezone.now()-datetime.timedelta(days=365)).date()
        self.assertEqual(self.user.profile.age, 1)

    """这个测试在没有输入出生日期的情况下出生年月"""
    def test_default_birth(self):
        self.assertEqual(self.user.profile.age, 45)