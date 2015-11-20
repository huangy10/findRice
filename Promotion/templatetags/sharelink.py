from django.template import Library
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
# from Promotion.models import Share
register = Library()


@register.simple_tag(name="share_link", takes_context=True)
def share_link(context, activity):
    return "deprecated"
    # user = context.get("user", None)
    # if user and not user.is_authenticated():
    #     user = None
    # try:
    #     share = Share.objects.get_or_create(activity=activity, user=user)[0]
    #     return share.get_share_link()
    # except ObjectDoesNotExist:
    #     return ""
    # except MultipleObjectsReturned:
    #     share = Share.objects.filter(activity=activity, user=user).first()
    #     Share.objects.filter(activity=activity, user=user).last().delete()
    #     return share.get_share_link()
