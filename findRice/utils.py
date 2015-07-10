
from django.core.exceptions import ValidationError


def field_is_active_validator(value):
    if not hasattr(value, "is_active"):
        return
    if not value.is_active:
        raise ValidationError("The related object is inactive")