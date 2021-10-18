from django import template

register = template.Library()


@register.filter
def format_contact_preference(value):
    if value == "BOTH":
        return "BOTH email and print"

    return value
