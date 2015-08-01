
from django.core.exceptions import ValidationError


def field_is_active_validator(value):
    if not hasattr(value, "is_active"):
        return
    if not value.is_active:
        raise ValidationError("The related object is inactive")


def choose_template_by_device(request, template_pc, template_mobile):
    if request.user_agent.is_pc:
        return template_pc
    else:
        return template_mobile