from django.contrib import admin

from .models import *


class ChoiceQuestionInline(admin.TabularInline):

    model = ChoiceQuestion
    extra = 0
    fields = ("question", "multi_choice", "choices_display")
    readonly_fields = ("choices_display", "question", "multi_choice")
    ordering = ("order_in_list",)

    def choices_display(self, obj):
        return Choice.objects.filter(question=obj).values_list("description", flat=True)

    choices_display.short_description = "Choices"

    def has_add_permission(self, request, **kwargs):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class NonChoiceQuestionInline(admin.TabularInline):

    model = NonChoiceQuestion
    extra = 0

    fields = ("question", "type")
    readonly_fields = ("question", "type")
    ordering = ("order_in_list", )

    def has_add_permission(self, request, **kwargs):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ["activity", "created_at", "is_active"]
    exclude = ("participants", "modified_at")
    inlines = [ChoiceQuestionInline, NonChoiceQuestionInline]
    list_filter = ("is_active", )
    search_fields = ("activity__name", )
    readonly_fields = ("activity", "created_at", "is_active")

