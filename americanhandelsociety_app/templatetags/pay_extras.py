from django import template

register = template.Library()


@register.filter
def format_membership_type(value):
    if value == "MESSIAH_CIRCLE":
        return "Messiah Circle (life membership)"

    return value.replace("_", " ").title()
