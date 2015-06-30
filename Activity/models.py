# coding=utf-8
import os
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils import timezone
# Create your models here.

DEFAULT_POSTER_PATH = os.path.join(settings.MEDIA_ROOT, 'defaultPosters', 'default.jpg')


class ActivityType(models.Model):
    """为了活动类型的可扩展性，这里将活动类型设定为一个类，由后台设置"""
    type_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)  # 类型描述应该精简
    display_order = models.IntegerField(default=0)  # 显示排序的按照这个值进行排序，如果出现相同的值，其属性可能会不稳定

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "活动类型"
        verbose_name_plural = "活动类型"


def get_activity_poster_path(act, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    time = act.created_at
    return "posters/%s/%s/%s/%s" % (time.year, time.month, time.day, filename)


class Activity(models.Model):
    """This class is an abstract of specific activity"""
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)   # 删除的适合将其设置为false即可
    activity_type = models.ManyToManyField(ActivityType)

    name = models.CharField(max_length=200, verbose_name="活动名称")
    host = models.ForeignKey(User, verbose_name="主办方")
    host_name = models.CharField(max_length=50, verbose_name="主办方名称")   # 注意这里的名称一开始是用User里面的名称填充的，但是可以修改

    location = models.CharField(max_length=200, verbose_name="活动地点")
    description = models.TextField(verbose_name="活动简介")

    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    last_length = models.IntegerField(verbose_name="持续时间(min)")

    reward = models.IntegerField(verbose_name="奖励金额")
    reward_for_share = models.IntegerField(default=5)       # 分享这个活动所得到的奖励
    # 其他用户经由分享链接完成活动时分享人获得的奖励比例
    reward_for_share_and_finished_percentage = models.FloatField(default=0.1)

    max_attend = models.IntegerField(verbose_name="允许报名的最大人数", default=10)
    min_attend = models.IntegerField(verbose_name="最少需要的人数", default=0)

    poster = models.ImageField(upload_to=get_activity_poster_path, verbose_name="海报",
                               default=DEFAULT_POSTER_PATH)
    recommended = models.BooleanField(default=False, verbose_name="热门推荐")
    recommended_level = models.IntegerField(default=0, verbose_name="推荐等级")          # 推荐等级，此值越高优先级越高，用于排序
    time_limited = models.BooleanField(default=False, verbose_name="限时报名")
    num_limited = models.BooleanField(default=False, verbose_name="限额报名")
    identified = models.BooleanField(default=False, verbose_name="是否认证")

    status = models.IntegerField(choices=(
        (0, "尚未开始"),
        (1, "已经开始"),
        (2, "已经结束"),
    ), default=0, verbose_name="活动状态")
    manually_start_time = models.DateTimeField(verbose_name="手动开始时间")
    manually_end_time = models.DateTimeField(verbose_name="手动结束时间")

    """下面是和活动关联的用户"""

    applied_by = models.ManyToManyField(User, related_name="applied_acts", through="AppliedBy",
                                        verbose_name="申请用户")
    denied = models.ManyToManyField(User, related_name="denied_acts", through="Denied",
                                    verbose_name="已拒绝的申请")
    approved = models.ManyToManyField(User, related_name="approved_acts", through="Approved",
                                      verbose_name="已批准的申请")
    liked_by = models.ManyToManyField(User, related_name="liked_acts", through="Like",
                                      verbose_name="关注的用户")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        cur = self.created_at
        if cur is None:
            cur = timezone.now()
        if not (cur <= self.start_time <= self.end_time):
            raise ValidationError("日期格式错误")

        super(Activity, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "活动"
        verbose_name_plural = "活动"


def active_required(method):
    """定义一个装饰器，来确保方法在执行前检查该类是否是active的，如果不是active的不执行方法"""
    def wrapper(self, *args):
        if not self.is_active:
            return
        else:
            return method(self, *args)
    return wrapper


class AppliedBy(models.Model):
    activity = models.ForeignKey(Activity, related_name="applied_by_relation")
    user = models.ForeignKey(User, related_name="applied_by_relation")

    apply_date = models.DateTimeField(auto_now_add=True, editable=False)

    is_active = models.BooleanField(default=True)

    @active_required
    def deny_this_apply(self, reason="未知原因"):
        """拒绝这个申请"""
        self.is_active = False
        self.save()
        deny = Denied.objects.get_or_create(activity=self.activity,
                                            user=self.user,
                                            deny_reason=reason)[0]
        if not deny.is_active:
            deny.is_active = True
            deny.save()

    @active_required
    def cancel_this_apply(self):
        """取消这次申请，这个由申请人发起"""
        self.is_active = False
        self.save()

    @active_required
    def approve_this_apply(self):
        self.is_active = False
        self.save()
        approve = Approved.objects.get_or_create(user=self.user,
                                                 activity=self.activity)[0]
        if not approve.is_active:
            approve.is_active = True
            approve.save()

    class Meta:
        verbose_name = "申请"
        verbose_name_plural = "申请"

        unique_together = ("activity", "user")


class Denied(models.Model):
    activity = models.ForeignKey(Activity, related_name="denied_relation")
    user = models.ForeignKey(User, related_name="denied_relation")

    deny_date = models.DateTimeField(auto_now=True, editable=False)
    deny_reason = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    @active_required
    def cancel_deny(self):
        """取消这次拒绝，恢复为申请状态"""
        self.is_active = False
        self.save()
        application = AppliedBy.objects.get(user=self.user,
                                            activity=self.activity,
                                            is_active=False)
        application.is_active = True
        application.save()

    class Meta:
        verbose_name = "拒绝"
        verbose_name_plural = "拒绝"

        unique_together = ("activity", "user")


class Approved(models.Model):
    activity = models.ForeignKey(Activity, related_name="approved_relation")
    user = models.ForeignKey(User, related_name="approved_relation")

    approve_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    @active_required
    def cancel_approve(self):
        self.is_active = False
        self.save()
        application = AppliedBy.objects.get(user=self.user,
                                            activity=self.activity,
                                            is_active=False)
        application.is_active=True
        application.save()

    class Meta:
        verbose_name = "批准"
        verbose_name_plural = "批准"

        unique_together = ("activity", "user")


class Like(models.Model):
    activity = models.ForeignKey(Activity, related_name="like_relation")
    user = models.ForeignKey(User, related_name="like_relation")

    like_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    @active_required
    def cancel_like(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = "喜欢"
        verbose_name_plural = "喜欢"

        unique_together = ("activity", "user")

