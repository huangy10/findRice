# coding=utf-8

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.db.models.signals import post_save

from Activity.models import Activity
from Welfare.models import WelfareGift
from .signals import send_notification
# Create your models here.


class NotificationCenter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="notification_center")

    @cached_property
    def unread_notifications_count(self):
        """未读的消息总数"""
        system_notification_num = SystemNotification.objects.filter(notification_center=self, read=False).count()
        activity_notification_num = ActivityNotification.objects.filter(notification_center=self, read=False).count()
        welfare_notification_num = WelfareNotification.objects.filter(notification_center=self, read=False).count()
        return system_notification_num + activity_notification_num + welfare_notification_num

    def __str__(self):
        return self.user.profile.name.encode("utf-8") + " 的消息中心"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_notification_center_automatically(sender, **kwargs):
    user = kwargs["instance"]
    created = kwargs["created"]
    if created:
        user.notification_center = NotificationCenter.objects.create(user=user)


@receiver(send_notification)
def send_notification_handler(sender, **kwargs):
    notification_type = kwargs["notification_type"]     # 取出消息的类型
    notification_center = kwargs["notification_center"]
    if notification_type == "system_notification":
        description = kwargs["description"]
        notification = SystemNotification.objects.create(notification_center=notification_center,
                                                         description=description)
        notification.save()
    elif notification_type == "activity_notification":
        activity = kwargs["activity"]
        user = None
        if "user" in kwargs:
            user = kwargs["user"]
        activity_notification_type = kwargs["activity_notification_type"]
        notification = ActivityNotification.objects.create(related_user=user,
                                                           related_activity=activity,
                                                           notification_center=notification_center,
                                                           notification_type=activity_notification_type)
        notification.save()
    else:
        activity = kwargs["activity"]
        gift = None
        if "gift" in kwargs:
            gift = kwargs["gift"]

        notification = WelfareNotification.objects.create(related_activity=activity,
                                                          gift=gift,
                                                          notification_center=notification_center)
        notification.save()


class Notification(models.Model):
    description = models.CharField(max_length=255, default="")
    read = models.BooleanField(default=False, verbose_name="是否已阅")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class SystemNotification(Notification):
    notification_center = models.ForeignKey(NotificationCenter, related_name="system_notifications")

    class Meta:
        verbose_name = "系统消息"
        verbose_name_plural = "系统消息"


class ActivityNotification(Notification):
    related_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    related_activity = models.ForeignKey(Activity)
    notification_center = models.ForeignKey(NotificationCenter, related_name="activity_notifications")

    notification_type = models.CharField(choices=(
        ("ready_requested", "就位确认"),
        ("apply_approved", "申请通过"),
        ("apply_full", "报名满"),
        ("ready_rejected", "拒绝就位"),
        ("share_finished", "分享完成")
    ), max_length=20, verbose_name="消息类型")

    def clean(self):
        """在clean函数中自动填充描述"""
        if self.notification_type == "ready_requested":
            self.description = "您报名的 %s，就绪确认" % self.related_activity.name
        elif self.notification_type == "apply_approved":
            self.description = "您报名的 %s，申请通过" % self.related_activity.name
        elif self.notification_type == "apply_full":
            self.description = "您的 %s，已报满" % self.related_activity.name
        elif self.notification_type == "ready_rejected":
            self.description = "您的 %s 中，申请人 %s 拒绝前往" % (self.related_activity.name, self.related_users.profile.name)
        else:
            self.description = "您推广的 %s，完成了活动 %s " % (self.related_users.profile.name, self.related_activity.name)

    def save(self, *args, **kwargs):
        if self.description == "":
            self.clean()
        super(ActivityNotification, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "通知"
        verbose_name_plural = "通知"


class WelfareNotification(Notification):
    gift = models.ForeignKey(WelfareGift, null=True)
    related_activity = models.ForeignKey(Activity, null=True)
    notification_center = models.ForeignKey(NotificationCenter, related_name="welfare_notifications")

    def clean(self):
        try:
            self.description = "您符合 %s 活动的要求，我们向您推荐" % self.related_activity.name
        except ObjectDoesNotExist:
            pass
        try:
            gift = self.gift
            self.description = "您符合 %s 活动的要求，我们向您赠送优惠卡" % self.related_activity.name
        except ObjectDoesNotExist:
            pass

    class Meta:
        verbose_name = "福利"
        verbose_name_plural = "福利"



