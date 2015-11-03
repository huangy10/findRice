# coding=utf-8
import os
import uuid
import hashlib

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from Activity.models import Activity
from Promotion.models import ShareRecord
from Promotion.signals import share_record_signal
from .tasks import create_zipped_avatar
# Create your models here.


def get_avatar_path(act, filename):
    ext = filename.split('.')[-1]
    filename = ("%s.%s" % (uuid.uuid4(), ext)).replace('-', '')
    time = act.created_at
    return "avatars/%s/%s/%s/%s" % (time.year, time.month, time.day, filename)


def get_avatar_path_zipped(act, filename):
    ext = filename.split('.')[-1]
    filename = ("%s.%s" % (uuid.uuid4(), ext)).replace('-', '')
    time = act.created_at
    return "avatars_zipped/%s/%s/%s/%s" % (time.year, time.month, time.day, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
    is_active = models.BooleanField(default=False, verbose_name="是否填写的了账户信息")
    name = models.CharField(max_length=50, default="")

    phoneNum = models.CharField(max_length=20, verbose_name="电话号码", default="")
    groupName = models.CharField(max_length=200, verbose_name="公司名称", default="")
    birthDate = models.DateField(verbose_name="出生日期", default="")

    @property
    def age(self):
        return (timezone.now().date()-self.birthDate).days / 365

    gender = models.CharField(choices=(
        ('m', '男'),
        ('f', '女'),
        ('u', '未知'),
    ), verbose_name="性别", max_length=2)
    avatar = models.ImageField(upload_to=get_avatar_path,
                               verbose_name="头像", null=True, blank=True)
    avatar_social = models.CharField(max_length=100, null=True, blank=True, verbose_name='社交平台头像URL')
    avatar_zipped = models.ImageField(upload_to=get_avatar_path_zipped, null=True, blank=True, editable=False)

    @property
    def avatar_url(self):
        if self.avatar_social and not self.avatar.name:
            return self.avatar_social
        else:
            if self.avatar_zipped:
                return self.avatar_zipped.url
            # 如果发现当前的profile没有生成压缩版的图像的话，那么开启一个异步线程生成压缩的图像，但是暂时返回原图
            # 这一步是为了兼容在引入压缩功能之前的图片
            # 实际进行压缩图片的生成是在创建和修改时
            elif self.avatar:
                create_zipped_avatar.delay(self)
                return self.avatar.url
            else:

                return '/media/' + settings.DEFAULT_PROFILE

    identified = models.BooleanField(default=False, verbose_name="是否认证")
    identified_date = models.DateField(verbose_name="认证日期", null=True, editable=False)

    coin = models.IntegerField(verbose_name="米币", default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    promotion_code = models.CharField(max_length=100, editable=False, null=True)

    def get_promotion_link(self):
        return "http://zhao-mi.net/register/basic?code=%s" % self.promotion_code

    def __str__(self):
        return self.user.username.encode("utf-8")

    # 米团系统重大修改，现在，每个用户最多只能拥有一名米团团长，而且必须在用户注册时指定
    team_leader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', verbose_name='米团长')

    def save(self, *args, **kwargs):

        if self.identified and self.identified_date is None:
            # 自动设置认证日期
            self.identified_date = timezone.now()
        if self.promotion_code is None:
            # 当用户还没有推广码时，创建一个新的。这个推广码将来会和这个用户永久的、唯一的绑定在一起
            raw_code = self.user.username + str(self.created_at) + "disturbing string"
            md5 = hashlib.md5(raw_code.encode('utf-8'))
            self.promotion_code = md5.hexdigest()
        super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "用户详情"
        verbose_name_plural = "用户详情"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_receiver(sender, **kwargs):
    user = kwargs["instance"]
    created = kwargs["created"]
    if created:         # 在创建一个user对象时为其生成一个profile
        user.profile = UserProfile.objects.create(user=user, gender="u",
                                                  birthDate=timezone.datetime(year=1970, month=1, day=1).date(),
                                                  name=user.username)
    else:
        user.profile.save()     # 在user保存以后总是保存其profile


class ContributionManager(models.Manager):

    def create(self, **kwargs):
        activity = kwargs['related_share_record'].activity
        kwargs['contributed_coin'] = activity.reward * activity.reward_for_share_and_finished_percentage
        return super(ContributionManager, self).create(**kwargs)


class RiceTeamContribution(models.Model):
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', verbose_name='米团长', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')

    contributed_coin = models.IntegerField(default=0, verbose_name='贡献的米币')
    activity = models.ForeignKey(Activity, verbose_name='相关活动')

    created_at = models.DateTimeField(auto_now_add=True)

    objects = ContributionManager()

    class Meta:
        verbose_name_plural = "米团贡献"
        verbose_name = "米团贡献"


class VerifyCode(models.Model):
    phoneNum = models.CharField(max_length=20, verbose_name="号码")
    code = models.CharField(max_length=6, verbose_name="验证码")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "验证码"
        verbose_name_plural = "验证码"

        ordering = ["-created_at"]




