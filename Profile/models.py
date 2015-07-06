# coding=utf-8
import os
import uuid

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
# Create your models here.

DEFAULT_PROFILE = "default_avatars/default_avatar.jpg"


def get_avatar_path(act, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    tz = timezone.get_current_timezone()
    time = tz.normalize(act.created_at)
    return "avatars/%s/%s/%s/%s" % (time.year, time.month, time.day, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
    is_active = models.BooleanField(default=False, verbose_name="是否填写的了账户信息")
    name = models.CharField(max_length=50, default="-")

    phoneNum = models.CharField(max_length=20, verbose_name="电话号码", default="-")
    groupName = models.CharField(max_length=200, verbose_name="公司名称", default="-")
    birthDate = models.DateField(verbose_name="出生日期",
                                 default=timezone.datetime(year=1970, month=1, day=1).date())

    @cached_property
    def age(self):
        tz = timezone.get_current_timezone()
        return (tz.normalize(timezone.now()).date()-self.birthDate).days / 365

    gender = models.CharField(choices=(
        ('m', '男'),
        ('f', '女'),
        ('u', '未知'),
    ), verbose_name="性别", default="u", max_length=2)
    avatar = models.ImageField(upload_to=get_avatar_path, default=DEFAULT_PROFILE,
                               verbose_name="头像")
    identified = models.BooleanField(default=False, verbose_name="是否认证")
    identified_date = models.DateField(verbose_name="认证日期", null=True, editable=False)

    coin = models.IntegerField(verbose_name="米币", default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.username.encode("utf-8")

    def save(self, *args, **kwargs):

        if self.identified and self.identified_date is None:
            self.identified_date = timezone.now()

        super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "用户详情"
        verbose_name_plural = "用户详情"


@receiver(share_record_signal)
def get_reward_from_share_record(sender, **kwargs):
    share_record = kwargs["share_record"]
    if not share_record.is_active:      # check if this share reward is valid
        return
    user = share_record.share.user
    if share_record.finished:
        user.profile.coin += share_record.actual_reward_for_finish
        user.rice_team.team_coin += share_record.actual_reward_for_finish
        contribution = RiceTeamContribution.objects.get_or_create(team=user.rice_team,
                                                                  user=share_record.target_user)[0]
        contribution.contributed_coin += share_record.actual_reward_for_finish
        contribution.save()
    else:
        user.profile.coin += share_record.actual_reward_for_share
        user.rice_team.team_coin += share_record.actual_reward_for_share
        contribution = RiceTeamContribution.objects.get_or_create(team=user.rice_team,
                                                                  user=share_record.target_user)[0]
        contribution.contributed_coin += share_record.actual_reward_for_share
        contribution.save()
    user.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_receiver(sender, **kwargs):
    user = kwargs["instance"]
    created = kwargs["created"]
    if created:         # 在创建一个user对象时为其生成一个profile
        user.profile = UserProfile.objects.create(user=user)
        # 以及一个米团
        user.rice_team = RiceTeam.objects.create(host=user)
    else:
        user.profile.save()     # 在user保存以后总是保存其profile


class RiceTeam(models.Model):
    host = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="米团主人", related_name="rice_team")       # 米团的主人
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="米团成员", through="RiceTeamContribution",
                                     related_name="rice_team_as_member")

    team_coin = models.IntegerField(default=0, verbose_name="团队米币")

    def total_members(self):
        return RiceTeamContribution.objects.filter(team=self).count()

    class Meta:
        verbose_name = "米团"
        verbose_name_plural = "米团"


class RiceTeamContribution(models.Model):
    team = models.ForeignKey(RiceTeam)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    contributed_coin = models.IntegerField(default=0)

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




