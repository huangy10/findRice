from django.template import Library
from django.core.urlresolvers import reverse

from Activity.models import Activity

register = Library()


@register.simple_tag(name='identification_act_url', takes_context=False)
def identification_act_url():
    act = Activity.objects.identification_act
    return reverse('activity_detail', args=[act.id, ])
