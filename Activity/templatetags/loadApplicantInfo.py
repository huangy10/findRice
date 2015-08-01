from django.template import Library
from django.core.exceptions import ObjectDoesNotExist

from Activity.models import ApplicationThrough

register = Library()


@register.simple_tag(name="load_applicant", takes_context=True)
def load_applicant(context, activity, user):
    """This function load the applicant data from the database and save it to the context"""
    try:
        context["applicant"] = ApplicationThrough.objects.get(activity=activity, user=user, is_active=True)
    except ObjectDoesNotExist:
        context["applicant"] = None
    return ""