from datetime import datetime, timezone

from django import template

from americanhandelsociety_app.models import Member

register = template.Library()


@register.filter
def show_renew_nav_item(value: Member):
    if value.date_of_last_membership_payment.year < datetime.now(timezone.utc).year:
        return True

    return False
