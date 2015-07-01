# coding=utf-8
import datetime
import re

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import IntegrityError

from .models import Share, ShareRecord
from Activity.models import Activity
# Create your tests here.


class ShareTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username="some_user")
        self.guest = get_user_model().objects.create(username="guest")
        self.activity = Activity.objects.create(
            name="test",
            host=self.user,
            location="here",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=2),
            last_length=60,
            reward=10,
            description="test",
            max_attend=10,
        )
        self.share = Share.objects.create(user=self.user,
                                          activity=self.activity)

    """测试分享链接生成"""

    def test_share_code_creation(self):
        self.assertIsNotNone(self.share.share_code)

    def test_share_link_creation(self):
        share_link = self.share.get_share_link()
        groups = re.match(r"^http://zhaomi.biz/action/(\d+)\?code=(\S+)$", share_link).groups()
        self.assertEqual(groups[0], str(self.share.activity_id))
        self.assertEqual(groups[1], self.share.share_code)

    """测试重复生成链接"""

    def test_create_share_twice(self):
        with self.assertRaises(IntegrityError):
            share = Share.objects.create(user=self.user,
                                         activity=self.activity)


class ShareRecordTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username="some_user")
        self.guest = get_user_model().objects.create(username="guest")
        self.activity = Activity.objects.create(
            name="test",
            host=self.user,
            location="here",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=2),
            last_length=60,
            reward=10,
            description="test",
            max_attend=10,
        )
        self.share = Share.objects.create(user=self.user,
                                          activity=self.activity)

    """测试用户通过分享链接进入的行为"""

    def test_respond_to_share(self):
        record = ShareRecord.objects.create(share=self.share, target_user=self.guest)
        self.assertFalse(record.finished)

    def test_respond_to_share_twice(self):
        record = ShareRecord.objects.create(share=self.share, target_user=self.guest)
        with self.assertRaises(IntegrityError):
            record = ShareRecord.objects.create(share=self.share, target_user=self.guest)


class CoinSystemTest(TestCase):
    """
    测试分享机制与米币系统
    这个部分综合了Share, ShareRecord, Activity, UserProfile等四个自定义类
    """

    def setUp(self):
        self.user = get_user_model().objects.create(username="some_user")
        self.guest = get_user_model().objects.create(username="guest")
        self.activity = Activity.objects.create(
            name="test",
            host=self.user,
            location="here",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=2),
            last_length=60,
            reward=10,
            description="test",
            max_attend=10,
        )
        self.share = Share.objects.create(user=self.user,
                                          activity=self.activity)

    def test_only_share_coin(self):
        """这个测试单次点击分享时各个表中的数据的一致性"""
        share_record = ShareRecord.objects.create(share=self.share,
                                                  target_user=self.guest)
        reward = self.activity.reward_for_share     # 分享应该得到的奖励
        self.assertEqual(self.share.total_reward, reward)   # 更新分享链接对象的total_reward，这个表示用户从这个分享中得到的奖励
        self.assertEqual(self.share.user.profile.coin, reward)  # 更新分享者的总奖励
        self.assertEqual(self.share.user.rice_team.team_coin, reward)   # 更新米团米币