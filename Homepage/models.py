# coding=utf-8
import uuid

from django.db import models
from django.utils import timezone

from Activity.models import Activity
# Create your models here.


def get_poster_path(act, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    tz = timezone.get_current_timezone()
    time = tz.normalize(timezone.now())
    return "homepage_posters/%s/%s/%s/%s" % (time.year, time.month, time.day, filename)


class HomepageIssueManager(models.Manager):

    def latest_issue(self):
        return self.all()[0]


class HomepageIssue(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    issue_num = models.IntegerField(default=1)

    objects = HomepageIssueManager()

    def save(self, *args, **kwargs):
        self.issue_num = HomepageIssue.objects.all().count() + 1
        super(HomepageIssue, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "首页"
        verbose_name_plural = "首页"
        ordering = ["-created_at"]


class HomepagePoster(models.Model):
    poster = models.ImageField(upload_to=get_poster_path, verbose_name="海报")
    related_activity = models.ForeignKey(Activity, verbose_name="相关活动")
    issue = models.ForeignKey(HomepageIssue)
    poster_type = models.IntegerField(choices=(
        (0, "banner"),
        (1, "footer")
    ))

    class Meta:
        verbose_name = "首页"
        verbose_name_plural = "首页"


