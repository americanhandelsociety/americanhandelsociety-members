import logging

from django.db.models import Q
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from americanhandelsociety_app.models import Member
from americanhandelsociety_app.utils import (
    today_is_first_of_month,
    is_january,
    is_december,
    year_now,
)

logger = logging.getLogger(__name__)

SUBJECT = "A Notification Concerning Your AHS Membership Renewal"
FROM = settings.DEFAULT_FROM_EMAIL


def assume_url():
    return (
        "http://0.0.0.0:8000"
        if settings.DEBUG
        else "https://www.americanhandelsociety.org"
    )


def determine_email_template(is_final_notice_month):
    if not is_final_notice_month:
        return "emails/overdue_payment.txt"
    return "emails/final_overdue_payment_notice.txt"


def collect_email_kwargs(is_final_notice_month):
    base = {"domain": assume_url()}
    if is_final_notice_month:
        year = year_now()
        base["next_year"] = year + 1
        base["this_year"] = year
    return base


def log_expected(members):
    logger.info(
        f"Found {members.count()} total users with overdue payments while preparing e-mail notification."
    )
    preface = "These are ids of users who will receive overdue payment e-mail notifications:\n\t"
    info = preface + "\n\t".join([str(m.id) for m in members])
    logger.info(info)


def send_overdue_payment_mail(
    members, email_template, email_kwargs, prepend_subject=False
):
    email_subject = f"Final Notice: {SUBJECT}" if prepend_subject else SUBJECT
    domain = assume_url()
    failed_ids = []
    for member in members:
        try:
            send_mail(
                email_subject,
                render_to_string(
                    email_template,
                    {
                        "first_name": member.first_name,
                        "last_name": member.last_name,
                        **email_kwargs,
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
    is_final_notice_month = is_december()
    log_expected(members)
    failures = send_overdue_payment_mail(
        members,
        determine_email_template(is_final_notice_month),
        collect_email_kwargs(is_final_notice_month),
        prepend_subject=is_final_notice_month,
    )
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
        if is_january():
            if today_is_first_of_month():
                logger.info(
                    "Is January: intentionally skipping e-mail sending this month."
                )
            return
        if today_is_first_of_month():
            send_and_log(Member.objects.dues_payment_pending())

    def handle(self, *args, **kwargs):
        self.send_overdue_payment_mail()
