from django.template import Library

register = Library()


@register.filter(name="list_num")
def list_num(acts):
    return len(acts)