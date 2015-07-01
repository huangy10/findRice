# coding=utf-8

import datetime
import os

from django.test import TestCase

from django.utils import timezone
from django.core.files import File
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Activity, ActivityType, get_activity_poster_path, DEFAULT_POSTER_PATH
from .models import AppliedBy, Approved, Like, Denied
# Create your tests here.


class ActivityModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username="some_user")
        self.default_activity_type = ActivityType.objects.create(type_name="default",
                                                                 description="default")
        self.test_poster_path = os.path.join(settings.BASE_DIR, "Activity", 'testFiles', "test1.jpg")
        poster = File(open(self.test_poster_path))
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
            poster=poster)
        self.activity.activity_type.add(self.default_activity_type)
        self.guest = get_user_model().objects.create(username="guest")

    """下面的五个Test主要测试海报部分的功能"""

    def test_representation(self):
        self.assertEqual(self.activity.name, str(self.activity))

    def test_poster_ext(self):
        ext = self.test_poster_path.split('.')[-1]
        img_path = str(self.activity.poster)
        img_ext = img_path.split('.')[-1]
        self.assertEqual(ext, img_ext)

    def test_poster_path(self):

        def get_path_from_uri(uri):
            path = uri.split('/')
            if len(path)>1:
                path = path[0:len(path)-1]
                return '/'.join(path)
            else:
                return uri

        path1 = get_path_from_uri(get_activity_poster_path(self.activity, self.test_poster_path))
        path2 = get_path_from_uri(str(self.activity.poster))
        self.assertEqual(path1, path2)

    def test_no_poster_name(self):
        activity = Activity.objects.create(
            name="another test",
            host=self.user,
            location="here",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=2),
            last_length=60,
            reward=10,
            description="test",
            max_attend=10,
        )
        activity.activity_type.add(self.default_activity_type)
        self.assertEqual(str(activity.poster), DEFAULT_POSTER_PATH)

    def test_duplicate_poster_name(self):
        poster = File(open(self.test_poster_path))
        act1 = Activity.objects.create(
            name="test",
            host=self.user,
            location="here",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=2),
            last_length=60,
            reward=10,
            description="test",
            max_attend=10,
            poster=poster)
        act1.activity_type.add(self.default_activity_type)
        act2 = Activity.objects.create(
            name="test",
            host=self.user,
            location="here",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=2),
            last_length=60,
            reward=10,
            description="test",
            max_attend=10,
            poster=poster)
        act2.activity_type.add(self.default_activity_type)
        self.assertNotEqual(act1.poster.name, act2.poster.name)

    """下面的测试对于几个时间属性进行测试"""

    def test_created_at_start_end_sequence(self):
        with self.assertRaises(ValidationError):
            act1 = Activity.objects.create(
                name="test",
                host=self.user,
                location="here",
                start_time=timezone.now()-datetime.timedelta(days=1),
                end_time=timezone.now() + datetime.timedelta(days=1),
                last_length=60,
                reward=10,
                description="test",
                max_attend=10,)
        with self.assertRaises(ValidationError):
            act1 = Activity.objects.create(
                name="test",
                host=self.user,
                location="here",
                start_time=timezone.now() - datetime.timedelta(days=1),
                end_time=timezone.now() - datetime.timedelta(days=2),
                last_length=60,
                reward=10,
                description="test",
                max_attend=10,)

    """下面测试中文支持"""

    def test_chinese_support(self):
        a = Activity.objects.create(
            name="测试",
            host=self.user,
            location="地点",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=1),
            last_length=60,
            reward=10,
            description="活动描述",
            max_attend=10)
        self.assertEqual(a.name, '测试')
        self.assertEqual(a.location, '地点')
        self.assertEqual(a.description, '活动描述')

    """下面测试活动和用户的关联的四个字段的功能"""

    def test_user_apply_an_activity(self):
        application = AppliedBy.objects.create(user=self.guest,
                                               activity=self.activity)
        # 然后通过活动检索到申请者
        candidate = get_user_model().objects.filter(applied_acts=self.activity)
        self.assertEqual(candidate[0], application.user)

        # 通过用户检索到其申请的活动
        activity = Activity.objects.filter(applied_by=self.guest)
        self.assertEqual(activity[0], application.activity)

    def test_user_apply_an_activity_twice(self):
        application = AppliedBy.objects.create(user=self.guest,
                                               activity=self.activity)
        with self.assertRaises(IntegrityError):
            application = AppliedBy.objects.create(user=self.guest,
                                               activity=self.activity)

    def test_cancel_an_apply(self):
        application = AppliedBy.objects.create(user=self.guest,
                                               activity=self.activity)
        application.cancel_this_apply()

        candidates = get_user_model().objects.filter(applied_acts=self.activity).exclude(applied_by_relation__is_active=False)
        # 取消之后应该为空
        self.assertEqual(len(candidates), 0)

    def test_apply_again_after_cancelled(self):
        """这个函数测试在取消一个申请之后再次申请，这时应该只存有一个条目"""
        application = AppliedBy.objects.create(user=self.guest,
                                               activity=self.activity)
        application.cancel_this_apply()
        another_apply = AppliedBy.objects.get_or_create(user=self.guest,
                                                        activity=self.activity)[0]
        if not another_apply.is_active:
            another_apply.is_active = True

        all_apply = AppliedBy.objects.filter(user=self.guest,
                                             activity=self.activity)
        self.assertEqual(len(all_apply), 1)

    def test_cancel_an_apply_twice(self):
        """注意到这里的没有写assert，功能正常的话会直接过，如果功能出现问题会报错"""
        application = AppliedBy.objects.create(user=self.guest,
                                               activity=self.activity)
        application.cancel_this_apply()
        application.cancel_this_apply()

    def test_user_deny_an_apply(self):
        application = AppliedBy.objects.create(user=self.guest,
                                               activity=self.activity)
        application.deny_this_apply()
        find_application = AppliedBy.objects.filter(user=self.guest,
                                                    activity=self.activity,
                                                    is_active=True)
        self.assertEqual(len(find_application), 0)
        deny = Denied.objects.filter(user=application.user,
                                     activity=application.activity,
                                     is_active=True)
        self.assertEqual(len(deny), 1)

    def test_deny_an_apply_twice(self):
        application = AppliedBy.objects.create(user=self.guest,
                                               activity=self.activity)
        application.deny_this_apply()
        application.deny_this_apply()

    def test_deny_reason(self):
        application = AppliedBy.objects.create(user=self.guest,
                                               activity=self.activity)
        application.deny_this_apply(u"测试")
        deny = Denied.objects.filter(user=application.user,
                                     activity=application.activity,
                                     is_active=True)[0]
        self.assertEqual(deny.deny_reason, u"测试")

    def test_approve_an_apply(self):
        # 发出一个申请
        application = AppliedBy.objects.create(activity=self.activity,
                                               user=self.guest)
        # 批准申请
        application.approve_this_apply()
        # 此时这个申请应该删除
        find_application = AppliedBy.objects.filter(user=self.guest,
                                                    activity=self.activity,
                                                    is_active=True)
        self.assertEqual(len(find_application), 0)
        # 同时查询允许的列表中应该新增这个条目
        approve = Approved.objects.filter(user=application.user,
                                          activity=application.activity,
                                          is_active=True)
        self.assertEqual(len(approve), 1)

    def test_approve_an_apply_twice(self):
        application = AppliedBy.objects.create(activity=self.activity,
                                               user=self.guest)
        # 批准申请
        application.approve_this_apply()
        application.approve_this_apply()

    def test_cancel_an_approve(self):
        """这个测试取消一个已经批准的申请，该申请将恢复到active状态，而approve本身会被删除"""
        # 发出一个申请
        application = AppliedBy.objects.create(activity=self.activity,
                                               user=self.guest)
        # 批准申请
        application.approve_this_apply()
        approve = Approved.objects.filter(user=application.user,
                                          activity=application.activity,
                                          is_active=True)[0]
        approve.cancel_approve()
        self.assertFalse(approve.is_active)
        application = AppliedBy.objects.get(activity=self.activity,
                                            user=self.guest)
        self.assertTrue(application.is_active)

    def test_cancel_an_approve_twice(self):
        # 发出一个申请
        application = AppliedBy.objects.create(activity=self.activity,
                                               user=self.guest)
        # 批准申请
        application.approve_this_apply()
        application.approve_this_apply()

    def test_like_an_approve(self):
        like = Like.objects.create(user=self.guest,
                                   activity=self.activity)
        # 通过用户检索到被like的活动
        act = Activity.objects.filter(liked_by=self.guest, like_relation__is_active=True)
        self.assertEqual(act[0], like.activity)
        # 通过活动检索到like这个活动的用户
        user = get_user_model().objects.filter(liked_acts=self.activity, like_relation__is_active=True)
        self.assertEqual(user[0], like.user)

    def test_cancel_like_an_approve(self):
        like = Like.objects.create(user=self.guest,
                                   activity=self.activity)
        like.cancel_like()
        user = get_user_model().objects.filter(liked_acts=self.activity, like_relation__is_active=True)
        self.assertEqual(len(user), 0)