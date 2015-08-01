# coding=utf-8
from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.


class WelfareGift(models.Model):
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='地址')        # 地址
    target = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='目标用户')                 # 目标用户
    coin_cost = models.IntegerField(default=0, verbose_name='扣除米币')                           # 抵扣的米币
    rmb = models.IntegerField(default=0, verbose_name='兑现的现金')                                # 兑现的人民币
    zfb_account = models.CharField(max_length=50, default='', verbose_name='支付宝账号')           # 支付宝账号
    getted = models.BooleanField(default=False, verbose_name='是否已经被领取或者兑现')

    getted_date = models.DateTimeField(null=True, blank=True, verbose_name='取现日期')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='申请兑换的日期')

    class Meta:
        verbose_name = '福利'
        verbose_name_plural = '福利'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.pk is not None and self.getted:
            origin = WelfareGift.objects.get(pk=self.pk)
            if not origin.getted:
                self.getted_date = timezone.now()
        super(WelfareGift, self).save(*args, **kwargs)
