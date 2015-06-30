# coding=utf-8
from django.db import models

from django.contrib.auth import get_user_model

from Activity.models import Activity
# Create your models here.


class Share(models.Model):
    user = models.ForeignKey(get_user_model())  # 发起分享的用户
    activity = models.ForeignKey(Activity)      # 被分享的活动

    total_reward_max = models.IntegerField(default=500)
    total_reward = models.IntegerField(default=0)   # 从这个分享中得到的奖励

    created_at = models.DateTimeField(auto_now_add=True)

    def get_share_link(self):
        pass

    class Meta:
        verbose_name = "分享"
        verbose_name_plural = "分享"

        unique_together = ("user", "activity")  # 显然一个用户对一个活动的分享行为应该是unique的


class ShareRecord(models.Model):
    share = models.ForeignKey(Share)    # 用户点击这个分享链接进入活动

    target_user = models.ForeignKey(get_user_model())   # 点击分享链接的用户

    create_at = models.DateTimeField(auto_now_add=True, verbose_name="分享日期")

    finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = "分享"
        verbose_name_plural = "分享"

        unique_together = ("share", "target_user")  # 显然一个用户点击一个分享链接只能记一次
