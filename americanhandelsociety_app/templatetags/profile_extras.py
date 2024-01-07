from django import template

register = template.Library()


@register.filter
def format_contact_preference(value):
    if value == "BOTH":
        return "BOTH email and print"

    return value


@register.filter
def format_publish_member_name_consent(value):
    if value == "YES":
        return "You granted permission to publish your name and membership tier."
    elif value == "NO":
        return "You did not grant permission to publish your name and membership tier."
    elif value == "ANONYMOUS":
        return 'You granted permission to publish your membership tier, but to display your name as "Anonymous."'
