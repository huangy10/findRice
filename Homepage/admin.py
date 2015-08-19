from django.contrib import admin

from .models import HomepageIssue, HomepagePoster
from Activity.models import Activity
# Register your models here.


class HomepagePosterInline(admin.StackedInline):
    model = HomepagePoster
    extra = 3

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'related_activity':
            kwargs['queryset'] = Activity.objects.filter(is_active=True)
        return super(HomepagePosterInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(HomepageIssue)
class HomepageIssueAdmin(admin.ModelAdmin):
    list_display = ["issue_num"]
    inlines = [HomepagePosterInline, ]

