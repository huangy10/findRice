import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import NotificationCenter, ActivityNotification, SystemNotification, WelfareNotification
from Activity.models import Activity
# Create your tests here.


class NotificationTest(TestCase):

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

    def test_notification_center_creation(self):
        center = self.user.notification_center

    def test_system_notification(self):
        notification = SystemNotification.objects.create(description="default",
                                                         notification_center=self.user.notification_center)
        self.assertEqual(self.user.notification_center.unread_notifications_count, 1)