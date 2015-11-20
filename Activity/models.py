# coding=utf-8
import os
import uuid
import copy

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property

from .tasks import create_zipped_poster, create_share_thumbnail
# Create your models here.


def get_activity_poster_path(act, filename):
    ext = filename.split('.')[-1]
    filename = ("%s.%s" % (uuid.uuid4(), ext)).replace("-", "")
    time = timezone.now()
    return "posters/%s/%s/%s/%s" % (time.year, time.month, time.day, filename)


def get_activity_poster_path_zipped(act, filename):
    ext = filename.split('.')[-1]
    filename = ("%s.%s" % (uuid.uuid4(), ext)).replace("-", "")
    time = timezone.now()
    return "posters_zipped/%s/%s/%s/%s" % (time.year, time.month, time.day, filename)


class ActivityType(models.Model):
    """为了活动类型的可扩展性，这里将活动类型设定为一个类，由后台设置"""
    type_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)  # 类型描述应该精简
    display_order = models.IntegerField(default=0, editable=False)  # 显示排序的按照这个值进行排序，如果出现相同的值，其属性可能会不稳定

    default_poster = models.ImageField(default=settings.DEFAULT_POSTER_PATH,
                                       verbose_name='默认海报',
                                       upload_to=get_activity_poster_path)
    default_poster_mobile = models.ImageField(default=settings.DEFAULT_POSTER_PATH,
                                              verbose_name='默认海报(mobile)',
                                              upload_to=get_activity_poster_path)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False, )

    def __str__(self):
        return self.type_name.encode("utf-8")

    def save(self, *args, **kwargs):
        if self.type_name == u'其他':
            self.display_order = 1
        else:
            self.display_order = 0

        super(ActivityType, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "活动类型"
        verbose_name_plural = "活动类型"
        ordering = ["display_order"]


class ActivityManager(models.Manager):

    @cached_property
    def identification_act(self):
        """申请成为认证用户的特殊活动
        """
        act = Activity.objects.filter(
            host__is_staff=True, host__is_superuser=True, is_active=True
        ).order_by('-created_at').first()
        return act

    @cached_property
    def identification_acts_id(self):
        acts = Activity.objects.filter(
            host__is_staff=True, host__is_superuser=True, is_active=True
        ).order_by('-created_at').values_list('id', flat=True)
        return acts


class Activity(models.Model):
    """This class is an abstract of specific activity"""
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)   # 删除的适合将其设置为false即可
    is_published = models.BooleanField(default=False)
    accept_apply = models.BooleanField(default=True)

    activity_type = models.ForeignKey(ActivityType, verbose_name='活动类型')

    name = models.CharField(max_length=200, verbose_name="活动名称")
    host = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="主办方")
    host_name = models.CharField(max_length=50, verbose_name="主办方名称")   # 注意这里的名称一开始是用User里面的名称填充的，但是可以修改

    location = models.CharField(max_length=200, verbose_name="活动地点")
    province = models.CharField(max_length=20, verbose_name="省份")
    city = models.CharField(max_length=100, verbose_name="城市")

    objects = ActivityManager()

    @property
    def loc_description(self):
        if self.city == u"全部地区":
            return self.province + self.location
        return self.province + self.city+self.location

    description = models.TextField(verbose_name="活动简介")

    @property
    def get_description(self):
        if self.reward_gift:
            return u"{0}\n礼品详情：{1}".format(self.description, self.reward_gift_detail)
        else:
            return self.description

    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    last_length = models.IntegerField(verbose_name="持续时间(min)")

    @property
    def day(self):
        return self.last_length / (60*24)

    @property
    def hour(self):
        return (self.last_length / 60) % 24

    @property
    def minute(self):
        return self.last_length % 60

    reward = models.IntegerField(verbose_name="奖励金额")
    # 分享这个活动所得到的奖励， 这个一个属性被废弃，但是暂时未删除，这个属性主要涉及到Promotion应用中对分享的处理
    reward_for_share = models.IntegerField(default=0)
    # 其他用户经由分享链接完成活动时分享人获得的奖励比例
    reward_for_share_and_finished_percentage = models.FloatField(default=0.1)
    # This property is the maximum share reward one user can get.
    # The administrator can change it. However, the new value won't affect the share records which are created before
    # the change
    reward_share_limit = models.IntegerField(default=500, verbose_name='分享奖励上限')
    # 是否包含礼品奖励
    reward_gift = models.BooleanField(default=False, verbose_name="礼品")
    reward_gift_detail = models.TextField(default="", verbose_name="礼品详情")

    @property
    def share_reward(self):
        return int(self.reward * self.reward_for_share_and_finished_percentage)

    @property
    def reward_description(self):
        """ 创建供模板使用的活动详情描述
        """
        if self.reward_gift and self.reward > 0:
            return u"￥"+str(self.reward)+u"+礼品"
        elif self.reward > 0 and not self.reward_gift:
            return u"￥"+str(self.reward)
        elif self.reward == 0 and self.reward_gift:
            return u"礼品"
        else:
            return u'￥0'


    max_attend = models.IntegerField(verbose_name="允许报名的最大人数", default=10)
    min_attend = models.IntegerField(verbose_name="最少需要的人数", default=0)

    poster = models.ImageField(upload_to=get_activity_poster_path, verbose_name="海报", null=True, blank=True)
    poster_zipped = models.ImageField(upload_to=get_activity_poster_path_zipped,
                                      verbose_name='压缩海报', null=True, blank=True)
    poster_thumbnail = models.ImageField(upload_to=get_activity_poster_path_zipped,
                                         verbose_name='海报缩略图', null=True, blank=True)

    @property
    def poster_url(self):
        # 尝试取出压缩图片，如果压缩图片不存在，则取出取出原图
        if self.poster_zipped:
            return self.poster_zipped.url
        elif self.poster:
            # 如果原图为空，则取出
            create_zipped_poster.delay(self)
            return self.poster.url
        else:
            return self.activity_type.default_poster.url

    @property
    def poster_thumbnail_url(self):
        if self.poster_thumbnail:
            return self.poster_thumbnail.url
        elif self.poster:
            create_share_thumbnail.delay(self)
            return self.poster.url
        else:
            return self.activity_type.default_poster_mobile.url

    recommended = models.BooleanField(default=False, verbose_name="热门推荐")
    recommended_level = models.IntegerField(default=0, verbose_name="推荐等级")          # 推荐等级，此值越高优先级越高，用于排序
    time_limited = models.BooleanField(default=False, verbose_name="限时报名")
    num_limited = models.BooleanField(default=False, verbose_name="限额报名")
    identified = models.BooleanField(default=False, verbose_name="是否认证")

    act_status = models.IntegerField(choices=(
        (0, "尚未开始"),
        (1, "已经开始"),
        (2, "已经结束"),
    ), default=0, verbose_name="活动状态")

    @property
    def status(self):
        now = timezone.now()
        if now < self.start_time:
            self.act_status = 0
        elif now < self.end_time:
            self.act_status = 1
        else:
            if self.act_status != 2:
                pass
            self.act_status = 2

        return self.act_status

    manually_start_time = models.DateTimeField(verbose_name="手动开始时间", null=True, editable=False)
    manually_end_time = models.DateTimeField(verbose_name="手动结束时间", null=True, editable=False)

    viewed_times = models.BigIntegerField(verbose_name="浏览次数", default=0)

    """下面是和活动关联的用户"""

    candidates = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ApplicationThrough",
                                        related_name="applied_activity")
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ActivityLikeThrough",
                                      related_name="liked_activity")

    """备份对象，注意备份对象应该总是in_active的"""
    backup = models.ForeignKey("self", related_name="master", null=True, blank=True)

    def __str__(self):
        return self.name.encode("utf-8")

    def get_duration_description(self):
        tz = timezone.get_current_timezone()
        return tz.normalize(self.start_time).strftime("%y/%m/%d %H:%M")+" - "+tz.normalize(self.end_time).strftime("%y/%m/%d %H:%M")

    def get_applying_num(self):
        return ApplicationThrough.objects.filter(activity=self, is_active=True,
                                                 status__in=["applying", "approved", "finished"]).count()

    def get_approved_num(self):
        return ApplicationThrough.objects.filter(activity=self, is_active=True,
                                                 status__in=["approved", "finished"]).count()

    def get_absolute_url(self):
        return reverse("detail", args=[str(self.id), ])

    def get_backup(self):
        if self.backup is None:
            tmp = copy.copy(self)
            tmp.id = None
            tmp.is_active = False
            tmp.save()
            self.backup = tmp
            self.save()
        return self.backup

    def save(self, *args, **kwargs):
        if self.poster is None:
            self.poster = self.activity_type.default_poster
        super(Activity, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "活动"
        verbose_name_plural = "活动"


class ActivityLikeThrough(models.Model):
    activity = models.ForeignKey(Activity, related_name="like_through")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="like_through")
    is_active = models.BooleanField(default=True)

    like_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(ActivityLikeThrough, self).save(*args, **kwargs)


class ApplicationThroughManager(models.Manager):

    def try_to_apply(self, **kwargs):
        act = kwargs["activity"]
        user = kwargs["user"]
        if act.status != 0 or not act.accept_apply:
            try:
                obj = super(ApplicationThroughManager, self).get(activity=act, user=user, is_active=True)
                return obj, False, "该活动无法申请，活动已完成或活动报名已关闭"
            except ObjectDoesNotExist:
                return None, False, "该活动无法申请，活动已完成或活动报名已关闭"
            except MultipleObjectsReturned:
                return None, False, "该活动无法申请，活动已完成或活动报名已关闭"
        else:
            obj, created = super(ApplicationThroughManager, self).get_or_create(activity=act, user=user)
            if not obj.is_active:
                obj.is_active = True
                obj.status = "applying"
                obj.apply_at = timezone.now()
                obj.save()
                return obj, True
            else:
                if created:
                    return obj, created, ''
                else:
                    return obj, created, "已经报名过该活动"


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

    objects = ApplicationThroughManager()

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
