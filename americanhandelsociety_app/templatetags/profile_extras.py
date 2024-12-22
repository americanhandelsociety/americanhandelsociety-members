from django import template
from django.utils.http import urlencode

from americanhandelsociety_app.constants import ZEFFY_EMBED_URL_FOR_RENEWAL_FORM

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


@register.simple_tag
def generate_renewal_url(member):
    params = {
        "modal": "true",
        "email": member.email,
        "firstName": member.first_name,
        "lastName": member.last_name,
    }
    encoded_params = urlencode(params)

    return f"{ZEFFY_EMBED_URL_FOR_RENEWAL_FORM}?{encoded_params}"
