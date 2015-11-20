# coding=utf-8
import hashlib
import logging

from django.db import models
from django.conf import settings

from Activity.utils import active_required
from Activity.models import Activity, ApplicationThrough
from .signals import share_record_signal
from findRice.utils import field_is_active_validator
# Create your modexls here.


class ShareRecord(models.Model):
    """ 在新的设计中，分享系统将和米币结算系统完全分离，即分享系统只用来记录分享行为本身的要素，
     而且由于米币结算系统和分享系统的解锁，故单独的分享code也不再需要，本APP的model简化为只需要ShareRecord
    """
    sharer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', verbose_name='被分享者')      # 分享着
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', verbose_name='分享着')        # 被分享着
    activity = models.ForeignKey(Activity, related_name='share_records')        # 被分享的活动
    share_time = models.DateTimeField(auto_now_add=True, verbose_name='分享日期')

    class Meta:
        verbose_name = u'分享记录'
        verbose_name_plural = u'分享记录'



