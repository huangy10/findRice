from django.contrib import admin

# Register your models here.
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "user", "is_active"]
    list_filter = ["is_active"]
    ordering = ["-created_at"]
    search_fields = ["name", "user__username"]