from django import template

register = template.Library()


@register.filter
def format_membership_type(value):
    if value == "JOINT":
        return "Joint (one set of publications)"
    if value == "SUBSCRIBER":
        return "Subscriber (institutions only)"

    return value.capitalize()
