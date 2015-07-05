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
from .models import ApplicationThrough
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
            poster=poster,
            activity_type=self.default_activity_type
        )
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
            activity_type=self.default_activity_type
        )
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
            poster=poster,
            activity_type=self.default_activity_type
        )

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
            poster=poster,
            activity_type=self.default_activity_type
        )

        self.assertNotEqual(act1.poster.name, act2.poster.name)

    """下面的测试对于几个时间属性进行测试"""

    def test_created_at_start_end_sequence(self):
        pass

    """下面测试中文支持"""

    def test_chinese_support(self):
        a = Activity.objects.create(
            name=u"测试",
            host_name=u"测试",
            host=self.user,
            location=u"地点",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=1),
            last_length=60,
            reward=10,
            description=u"活动描述",
            max_attend=10,
            activity_type=self.default_activity_type
        )
        self.assertEqual(a.name, u'测试')
        self.assertEqual(a.location, u'地点')
        self.assertEqual(a.description, u'活动描述')


class CandidatesThroughTest(TestCase):

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
            poster=poster,
            activity_type=self.default_activity_type
        )
        self.guest = get_user_model().objects.create(username="guest")

    def test_apply_an_activity(self):
        application = ApplicationThrough.objects.create(activity=self.activity,
                                                        user=self.guest)
        self.assertEqual(application.status, "applying")
        self.assertTrue(application.is_active)

    def test_apply_an_activity_twice(self):
        application = ApplicationThrough.objects.create(activity=self.activity,
                                                        user=self.guest)
        with self.assertRaises(IntegrityError):
            application = ApplicationThrough.objects.create(activity=self.activity,
                                                            user=self.guest)

    def test_deny_an_activity(self):
        application = ApplicationThrough.objects.create(activity=self.activity,
                                                        user=self.guest)
        application.status = "denied"

    def test_approve_an_activity(self):
        application = ApplicationThrough.objects.create(activity=self.activity,
                                                        user=self.guest)
        application.status = "approved"

    def test_finish_an_activity(self):
        """注意在活动结束时的自动结算在Promotion.tests的测试中进行"""
        application = ApplicationThrough.objects.create(activity=self.activity,
                                                        user=self.guest)
        application.status = "finish"