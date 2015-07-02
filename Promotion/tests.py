# coding=utf-8
import datetime
import re
import random

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import IntegrityError

from .models import Share, ShareRecord
from Activity.models import Activity, ApplicationThrough
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

    def test_share_coin_consistence(self):
        """这个测试单次点击分享时各个表中的数据的一致性"""
        share_record = ShareRecord.objects.create(share=self.share,
                                                  target_user=self.guest)
        reward = self.activity.reward_for_share     # 分享应该得到的奖励
        self.assertEqual(self.share.total_reward, reward)   # 更新分享链接对象的total_reward，这个表示用户从这个分享中得到的奖励
        self.assertEqual(self.share.user.profile.coin, reward)  # 更新分享者的总奖励
        self.assertEqual(self.share.user.rice_team.team_coin, reward)   # 更新米团米币
        new_guest = get_user_model().objects.create(username="another user")
        new_share_record = ShareRecord.objects.create(share=self.share,
                                                      target_user=new_guest)
        self.assertEqual(self.share.total_reward, 2*reward)   # 更新分享链接对象的total_reward，这个表示用户从这个分享中得到的奖励
        self.assertEqual(self.share.user.profile.coin, 2*reward)  # 更新分享者的总奖励
        self.assertEqual(self.share.user.rice_team.team_coin, 2*reward)   # 更新米团米币

    def test_share_finish_coin(self):
        share_record = ShareRecord.objects.create(share=self.share,
                                                  target_user=self.guest)
        reward = self.activity.reward_for_share     # 分享应该得到的奖励
        self.assertEqual(self.share.total_reward, reward)   # 更新分享链接对象的total_reward，这个表示用户从这个分享中得到的奖励
        self.assertEqual(self.share.user.profile.coin, reward)  # 更新分享者的总奖励
        self.assertEqual(self.share.user.rice_team.team_coin, reward)   # 更新米团米币
        share_record.finished = True
        share_record.save()
        reward_for_finished = self.activity.reward_for_share_and_finished_percentage * self.activity.reward
        self.assertEqual(self.share.total_reward, reward+reward_for_finished)   # 更新分享链接对象的total_reward，这个表示用户从这个分享中得到的奖励
        self.assertEqual(self.share.user.profile.coin, reward+reward_for_finished)  # 更新分享者的总奖励
        self.assertEqual(self.share.user.rice_team.team_coin, reward+reward_for_finished)   # 更新米团米币

    def test_reward_reaches_max_limit(self):
        for i in range(0, 200):
            user = get_user_model().objects.create(username=str(i))
            share_record = ShareRecord.objects.create(share=self.share,
                                                      target_user=user)
            if random.random() > 0.5:
                share_record.finished = True
            share_record.save()
        self.assertEqual(self.share.total_reward, self.share.total_reward_max)
        self.assertEqual(self.share.user.profile.coin, self.share.total_reward_max)
        self.assertEqual(self.share.user.rice_team.team_coin, self.share.total_reward_max)

    def test_auto_settlement(self):
        """测试自动结算"""
        # 点击进入活动，生成记录
        share_record = ShareRecord.objects.create(share=self.share,
                                                  target_user=self.guest)
        reward = self.activity.reward_for_share     # 分享应该得到的奖励
        reward_for_finished = self.activity.reward_for_share_and_finished_percentage * self.activity.reward
        # 成功进入活动，注意问卷填写与检查不在这里测试范围之内
        application = ApplicationThrough.objects.create(activity=self.activity,
                                                        user=self.guest)
        application.share_record = share_record
        application.status = "approved"  # 允许其参加
        application.status = "finished"  # 成功结束活动
        application.save()
        self.assertEqual(self.share.total_reward, reward+reward_for_finished)   # 更新分享链接对象的total_reward，这个表示用户从这个分享中得到的奖励
        self.assertEqual(self.share.user.profile.coin, reward+reward_for_finished)  # 更新分享者的总奖励
        self.assertEqual(self.share.user.rice_team.team_coin, reward+reward_for_finished)   # 更新米团米币

    def test_two_share_consistence(self):
        """测试发起两个分享时，米币数据的一致性"""
        # 再生成一个活动
        another_activity = Activity.objects.create(
            name="test",
            host=self.user,
            location="here",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=2),
            last_length=60,
            reward=20,
            reward_for_share=6,
            reward_for_share_and_finished_percentage=0.07,
            description="test",
            max_attend=10,
        )
        another_share = Share.objects.create(user=self.user,
                                             activity=another_activity)
        for i in range(0, 5):
            user = get_user_model().objects.create(username=str(i))
            share_record = ShareRecord.objects.create(share=self.share,
                                                      target_user=user)
            if i == 3:
                share_record.finished = True
            share_record.save()

        for i in range(5, 10):
            user = get_user_model().objects.create(username=str(i))
            share_record = ShareRecord.objects.create(share=another_share,
                                                      target_user=user)
            if i == 9:
                share_record.finished = True
            share_record.save()
        activity = self.share.activity
        reward_for_share = 5 * activity.reward_for_share + \
            activity.reward * activity.reward_for_share_and_finished_percentage
        reward_for_another_share = 5 * another_activity.reward_for_share + \
            another_activity.reward * another_activity.reward_for_share_and_finished_percentage
        reward = reward_for_share + reward_for_another_share

        self.assertEqual(self.share.total_reward, reward_for_share)   # 更新分享链接对象的total_reward，这个表示用户从这个分享中得到的奖励
        self.assertEqual(another_share.total_reward, reward_for_another_share)
        self.assertEqual(self.share.user.profile.coin, reward)  # 更新分享者的总奖励
        self.assertEqual(self.share.user.rice_team.team_coin, reward)   # 更新米团米币