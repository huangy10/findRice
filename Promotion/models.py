# coding=utf-8
import hashlib
import logging

from django.db import models
from django.conf import settings

from Activity.utils import active_required
from Activity.models import Activity, ApplicationThrough
from .signals import share_record_signal
from findRice.utils import field_is_active_validator
# Create your models here.


logger = logging.getLogger(__name__)


class Share(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, validators=[field_is_active_validator], null=True, blank=True)  # 发起分享的用户
    activity = models.ForeignKey(Activity, validators=[field_is_active_validator])      # 被分享的活动

    @property
    def total_reward_max(self):
        return self.activity.reward_share_limit

    total_reward = models.IntegerField(default=0)   # 从这个分享中得到的奖励

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    share_code = models.CharField(max_length=100, editable=False, null=True)

    def get_share_link(self):
        return settings.FR_SHARE_LINK_TEMPLATE % (self.activity_id, self.share_code)

    def save(self, *args, **kwargs):
        if self.share_code is None:     # Generate the share code when saved for the first time
            def get_share_code():
                if self.user is None:
                    raw_code = u"anonymous user " + str(self.activity.id) +"disturbing string"
                else:
                    raw_code = self.user.username+str(self.activity.id)+"disturbing string"
                md5 = hashlib.md5(raw_code.encode('utf-8'))
                return md5.hexdigest()
            self.share_code = get_share_code()
        super(Share, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "分享"
        verbose_name_plural = "分享"

        unique_together = ("user", "activity")  # 显然一个用户对一个活动的分享行为应该是unique的


class ShareRecordManager(models.Manager):

    def create(self, **kwargs):
        obj = super(ShareRecordManager, self).create(**kwargs)
        if obj.share.user is None:
            return obj

        def get_actual_reward():
	    if obj.share.user == obj.share.activity.host:
		logger.debug(u'分享自己创建的活动，不结算米币，发起分享的用户是%s' % obj.share.user.username)
                return
            cur_share_reward = obj.share.total_reward          # 取出当前奖励
            cur_share_reward += obj.share.activity.reward_for_share    # 计算增加奖励
            cur_share_reward = min(cur_share_reward, obj.share.total_reward_max)   # 上限截断
            obj.actual_reward_for_share = cur_share_reward - obj.share.total_reward  # 实际增加的奖励
            obj.share.total_reward = cur_share_reward

        get_actual_reward()
        obj.save()
        share_record_signal.send(sender=ShareRecord, share_record=obj)
        return obj

    def get_or_create(self, **kwargs):

        share = kwargs["share"]
        target_user = kwargs["target_user"]
        if share.user == target_user or share.activity.host == target_user:
            # 如果发起分享这和点击分享链接的是同一人，不予创建分享链接
            return None, False

        obj, created = super(ShareRecordManager, self).get_or_create(**kwargs)
        if not created:
            return obj, created

        if obj.share.user is None:
            return obj, created

        def get_actual_reward():
	    if obj.share.user == obj.share.activity.host:
		logger.debug(u'分享自己创建的活动，不结算米币，发起分享的用户是%s' % obj.share.user.username)
                return
            cur_share_reward = obj.share.total_reward          # 取出当前奖励
            cur_share_reward += obj.share.activity.reward_for_share    # 计算增加奖励
            cur_share_reward = min(cur_share_reward, obj.share.total_reward_max)   # 上限截断
            obj.actual_reward_for_share = cur_share_reward - obj.share.total_reward  # 实际增加的奖励
            obj.share.total_reward = cur_share_reward

        get_actual_reward()
        obj.save()
        share_record_signal.send(sender=ShareRecord, share_record=obj)
        return obj, created


class ShareRecord(models.Model):
    share = models.ForeignKey(Share, validators=[field_is_active_validator])    # 用户点击这个分享链接进入活动
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, validators=[field_is_active_validator])   # 点击分享链接的用户
    application = models.OneToOneField(ApplicationThrough, related_name="share_record", null=True, default=None,
                                       validators=[field_is_active_validator])   # this field is temperately deprecated

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="分享日期")

    finished = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    actual_reward_for_share = models.IntegerField(default=0)
    actual_reward_for_finish = models.IntegerField(default=0)

    objects = ShareRecordManager()

    @active_required
    def save(self, *args, **kwargs):
        if self.finished and self.share.user is not None:

            def get_actual_reward():
                if self.share.user == self.share.activity.host:
                    self.actual_reward_for_finish = 0
                    self.actual_reward_for_share = 0
                    logger.debug(u'分享自己创建的活动，不结算米币，发起分享的用户是%s' % self.share.user.username)
                    return
                cur_share_reward = self.share.total_reward          # 取出当前奖励
                cur_share_reward += self.share.activity.reward * \
                    self.share.activity.reward_for_share_and_finished_percentage    # 计算增加奖励
                cur_share_reward = min(cur_share_reward, self.share.total_reward_max)   # 上限截断
                self.actual_reward_for_finish = cur_share_reward - self.share.total_reward  # 实际增加的奖励
                self.share.total_reward = cur_share_reward

            get_actual_reward()
        super(ShareRecord, self).save(*args, **kwargs)
        if self.finished and self.share.user is not None:
            share_record_signal.send(sender=ShareRecord, share_record=self)
            self.is_active = False

    class Meta:
        verbose_name = "分享"
        verbose_name_plural = "分享"

        unique_together = ("share", "target_user")  # 显然一个用户点击一个分享链接只能记一次
