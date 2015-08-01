from django.template import Library
from django.core.exceptions import ObjectDoesNotExist

from Activity.models import ActivityLikeThrough

register = Library()

@register.simple_tag(name="load_like", takes_context=True)
def load_like(context, activity, user):
    context["like"] = None
    if user is None or not user.is_authenticated():
        return ""
    try:
        context["like"] = ActivityLikeThrough.objects.get(activity=activity,
                                                          user=user,
                                                          is_active=True)
    except ObjectDoesNotExist:
        pass
    return ""
