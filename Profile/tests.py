# coding=utf-8
import datetime
import json
import random
import os

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import UserProfile, VerifyCode
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


class UserProfileLoginTest(TestCase):
    """ 这个测试测试重新修改的注册登陆系统的完整性和安全性
    """

    def setUp(self):
        user = User.objects.create(username='15201525181')
        user.set_password('huang9040601')
        user.save()
        self.user = user

    def test_login(self):
        self.client.get(reverse('profile:login'))
        response = self.client.post(reverse('profile:login'), data=dict(
            csrf_token=self.client.cookies['csrftoken'],
            username='15201525181',
            pwd='huang9040601'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, {'success': True, 'data': {'url': '/'}})

    def test_login_with_wrong_password(self):
        self.client.get(reverse('profile:login'))
        response = self.client.post(reverse('profile:login'), data=dict(
            csrf_token=self.client.cookies['csrftoken'],
            username='15201525181',
            pwd='wrong_pwd'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, {'success': False, 'data': {'pwd': u'密码错误'}})

    def test_login_with_invalid_username(self):
        self.client.get(reverse('profile:login'))
        response = self.client.post(reverse('profile:login'), data=dict(
            csrf_token=self.client.cookies['csrftoken'],
            username='15201525182',
            pwd='huang9040601'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, {'success': False, 'data': {'username': u'该用户名不存在'}})


class UserProfileRegisterTest(TestCase):

    def create_random_code(self, phone):
        # 由于在这里无法直接测试线上的短信系统，故这里模拟其行为，先创建一条记录
        code = ''
        for _ in range(6):
            code = random.choice('0123456789')
        VerifyCode.objects.create(phoneNum=phone, code=code)
        return code

    def test_register(self):
        code = self.create_random_code(phone='15201525181')
        self.client.get(reverse('profile:register'))
        response = self.client.post(reverse('profile:register'), data={
            'phone_num': '15201525181',
            'password1': 'huangyan14',
            'password2': 'huangyan14',
            'avatar': open(os.path.join(settings.BASE_DIR, 'media', 'test', 'test.jpg')),
            'code': code,
            'nickname': 'Zhaomi',
            'share_code': '',
            'csrf_token': self.client.cookies['csrftoken']
        })
        response_data = json.loads(response.content)
        self.assertEqual(response_data, {'success': True, 'data': {'url': '/'}})
