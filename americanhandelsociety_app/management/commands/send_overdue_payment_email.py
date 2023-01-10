import logging
from functools import wraps
import time

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail
from django.conf import settings
from django.template.loader import render_to_string

from americanhandelsociety_app.models import Member
from americanhandelsociety_app.utils import year_now

logger = logging.getLogger(__name__)

SUBJECT = "A Notification Concerning Your AHS Membership Renewal"
FROM = settings.DEFAULT_FROM_EMAIL


def assume_url():
    return (
        "http://0.0.0.0:8000"
        if settings.DEBUG
        else "https://www.americanhandelsociety.org"
    )


def get_members_with_overdue_payments():
    return Member.objects.exclude(
        membership_type=Member.MembershipType.MESSIAH_CIRCLE
    ).filter(date_of_last_membership_payment__year__lt=year_now())


def send_overdue_payment_mail(members):
    domain = assume_url()
    recipient_count = send_mass_mail(
        [
            (
                SUBJECT,
                render_to_string(
                    "emails/overdue_payment.txt",
                    {"domain": domain, "first_name": m.first_name},
                ),
                FROM,
                [m.email],
            )
            for m in members
        ],
        fail_silently=False,
    )


class Command(BaseCommand):
    help = "Send a renewal e-mail."

    def add_arguments(self, parser):
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Skip print count and ID of users receiving e-mail. Does not send. No PII.",
        )

    def print_info(self, members_with_overdue_payments):
        print(
            f"Found {members_with_overdue_payments.count()} users with overdue payments."
        )
        preface = "These are ids of users who will receive notifications:\n\t"
        info = preface + "\n\t".join([m.id for m in members_with_overdue_payments])
        print(info)

    def send_overdue_payment_mail(self, quiet=False):
        members_with_overdue_payments = get_members_with_overdue_payments()
        if not quiet:
            self.print_info(members_with_overdue_payments)
        send_overdue_payment_mail(members_with_overdue_payments)

    def handle(self, *args, **kwargs):
        self.send_overdue_payment_mail(**kwargs)
