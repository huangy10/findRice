# coding=utf-8
from django.contrib import admin

from .models import Activity, ActivityType
# Register your models here.


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'host', 'start_time', 'end_time', 'is_active', 'created_at']
    list_filter = ("is_active", )
    ordering = ['created_at']
    actions = ["deactivate_activity"]
    search_fields = ["name", "host__profile__name"]

    def deactivate_activity(self, request, query_set):
        count = query_set.update(is_active=False)
        self.message_user(request, "总共撤消了 %s 个活动" % count)

    deactivate_activity.short_description = "撤销活动"


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ["type_name", "description"]
    ordering = ["display_order"]
    exclude = ["created_at", "modified_at"]
