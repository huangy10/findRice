from django.contrib import admin

from .models import HomepageIssue, HomepagePoster
# Register your models here.


class HomepagePosterInline(admin.StackedInline):
    model = HomepagePoster
    extra = 3


@admin.register(HomepageIssue)
class HomepageIssueAdmin(admin.ModelAdmin):
    list_display = ["issue_num"]
    inlines = [HomepagePosterInline, ]