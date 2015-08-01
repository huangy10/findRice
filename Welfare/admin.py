# coding=utf-8
from django.contrib import admin
from django.utils import timezone

from .models import WelfareGift


# Register your models here.

@admin.register(WelfareGift)
class WelfareGiftAdmin(admin.ModelAdmin):
    list_display = ('target', 'zfb_account', 'rmb', 'coin_cost', 'getted', 'getted_date', 'created_at')
    list_filter = ('getted', )
    ordering = ('-created_at', )
    actions = ('confirm_payed', )
    search_fields = ('target__profile__name', 'zfb_account')

    def confirm_payed(self, request, query_set):
        count = query_set.update(getted=True, getted_date=timezone.now())
        self.message_user(request, "总共兑换了 %s 个申请" % count)
    confirm_payed.short_description = '确认兑换'