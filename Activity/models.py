# coding=utf-8
import os
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
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

    def __str__(self):
        return self.type_name.encode("utf-8")

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
    activity_type = models.ForeignKey(ActivityType)

    name = models.CharField(max_length=200, verbose_name="活动名称")
    host = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="主办方")
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
    manually_start_time = models.DateTimeField(verbose_name="手动开始时间", null=True)
    manually_end_time = models.DateTimeField(verbose_name="手动结束时间", null=True)

    """下面是和活动关联的用户"""

    candidates = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ApplicationThrough",
                                        related_name="applied_activity")
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ActivityLikeThrough",
                                      related_name="liked_activity")

    def __str__(self):
        return self.name.encode("utf-8")

    def get_duration_description(self):
        return self.start_time.strftime("%y/%m/%d %H:%M")+" - "+self.end_time.strftime("%y/%m/%d")

    def get_applying_num(self):
        return ApplicationThrough.objects.filter(activity=self,
                                                 status="applying").count()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "活动"
        verbose_name_plural = "活动"


class ActivityLikeThrough(models.Model):
    activity = models.ForeignKey(Activity, related_name="like_through")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="like_through")

    like_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(ActivityLikeThrough, self).save(*args, **kwargs)


class ApplicationThrough(models.Model):
    """这个类是对活动的申请的抽象"""
    activity = models.ForeignKey(Activity, related_name="applications_through")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="applications_through")

    apply_at = models.DateTimeField(verbose_name="申请日期", auto_now_add=True)  # 这个属性为该对象的创建日期，也就代表了最早的申请
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    status = models.CharField(choices=(
        ("applying", "申请中"),
        ("approved", "已批准"),
        ("ready", "已就位"),
        ("denied", "已拒绝"),
        ("finished", "已完成")
    ), default="applying", max_length=10, verbose_name="状态")
    is_active = models.BooleanField(default=True, help_text="don't set this manually")

    def save(self, *args, **kwargs):
        super(ApplicationThrough, self).save(*args, **kwargs)
        if self.status == "finished":
            try:
                self.share_record.finished = True
                self.share_record.save()
            except ObjectDoesNotExist:
                pass

    class Meta:
        verbose_name = "参与"
        verbose_name_plural = "参与"
        unique_together = ["activity", "user"]
        ordering = ["-apply_at"]


class ActivityVisitRecord(models.Model):
    """用户访问活动历史记录"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    activity = models.ForeignKey(Activity)

    visit_date = models.DateTimeField(auto_now_add=True)
    visit_ip = models.GenericIPAddressField(default="0.0.0.0")
    visit_location = models.CharField(max_length=255, default="-")
    visit_device = models.CharField(max_length=255, default="-")

    class Meta:
        verbose_name = "访问记录"
        verbose_name_plural = "访问记录"