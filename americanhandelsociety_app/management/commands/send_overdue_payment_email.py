import logging

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
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


def log_expected(members):
    logger.info(f"Found {members.count()} total users with overdue payments.")
    preface = "These are ids of users who will receive notifications:\n\t"
    info = preface + "\n\t".join([str(m.id) for m in members])
    logger.info(info)


def send_overdue_payment_mail(members):
    domain = assume_url()
    failed_ids = []
    for member in members:
        try:
            send_mail(
                SUBJECT,
                render_to_string(
                    "emails/overdue_payment.txt",
                    {
                        "domain": domain,
                        "first_name": member.first_name,
                        "last_name": member.last_name,
                    },
                ),
                FROM,
                [member.email],
                fail_silently=False,
            )
        except Exception as exc:
            logger.info(f"Sending mail failed with {type(exc)}. Details: {exc}.")
            failed_ids.append(member.id)
    return failed_ids


def send_and_log(members):
    log_expected(members)
    failures = send_overdue_payment_mail(members)
    failed_count = len(failures)
    sent_count = len(members) - failed_count
    base = f"Sent a total of {sent_count} emails, with {failed_count} failures."
    if failures:
        base = (
            base
            + " IDs of members whose e-mail sending failed:\n\t"
            + "\n\t".join(failed_ids)
        )
    logger.info(base)
    return sent_count


class Command(BaseCommand):
    help = "Send renewal e-mail to each overdue member."

    def send_overdue_payment_mail(self):
        members_with_overdue_payments = get_members_with_overdue_payments()
        sent_count = send_and_log(members_with_overdue_payments)

    def handle(self, *args, **kwargs):
        self.send_overdue_payment_mail()
