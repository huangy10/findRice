# coding=utf-8
import os
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.functional import cached_property
from django.utils import timezone

from Activity.models import Activity
# Create your models here.

DEFAULT_PROFILE = os.path.join(settings.MEDIA_ROOT, 'default_avatars', 'default_avatar.jpg')


def get_avatar_path(act, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    tz = timezone.get_current_timezone()
    time = tz.normalize(act.created_at)
    return "avatars/%s/%s/%s/%s" % (time.year, time.month, time.day, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    name = models.CharField(max_length=50)

    phoneNum = models.CharField(max_length=20, verbose_name="电话号码", default="-")
    groupName = models.CharField(max_length=200, verbose_name="公司名称", default="-")
    birthDate = models.DateField(verbose_name="出生日期",
                                 default=timezone.datetime(year=1970, month=1, day=1).date())

    @cached_property
    def age(self):
        tz = timezone.get_current_timezone()
        return (tz.normalize(timezone.now()).date()-self.birthDate).days / 365

    gender = models.SmallIntegerField(choices=(
        (0, '男'),
        (1, '女'),
        (2, '保密'),
    ), verbose_name="性别", default=2)
    avatar = models.ImageField(upload_to=get_avatar_path, default=DEFAULT_PROFILE,
                               verbose_name="头像")
    identified = models.BooleanField(default=False, verbose_name="是否认证")
    identified_date = models.DateField(verbose_name="认证日期", null=True)

    coin = models.IntegerField(verbose_name="米币", default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["created_at"]
        verbose_name = "用户详情"
        verbose_name_plural = "用户详情"

