from unittest.mock import call, patch, ANY
from smtplib import SMTPException

import pytest

from americanhandelsociety_app.management.commands.send_overdue_payment_email import (
    send_overdue_payment_mail,
    Command,
)
from americanhandelsociety_app.models import Member
from americanhandelsociety_app.utils import year_now

from time_machine import travel

############
# DEFAULTS #
############

DEFAULT_TEMPLATE = "emails/overdue_payment.txt"
DEFAULT_DOMAIN = {"domain": "https://www.americanhandelsociety.org"}

###########
# PATCHES #
###########


# Most of the pytest fixtures can be found in
# tests/conftest.py. However, these fixtures are
# dependent on patch paths relevant to the tests
# in this particular file, thus these fixtures here.
@pytest.fixture
def mock_send_and_log():
    with patch(
        "americanhandelsociety_app.management.commands.send_overdue_payment_email.send_and_log",
        return_value=0,
        autospec=True,
    ) as mock:
        yield mock


@pytest.fixture
def mock_send_mail_in_command():
    with patch(
        "americanhandelsociety_app.management.commands.send_overdue_payment_email.send_mail",
        return_value=0,
        autospec=True,
    ) as mock:
        yield mock


@pytest.fixture
def mock_email_command_logger():
    with patch(
        "americanhandelsociety_app.management.commands.send_overdue_payment_email.logger",
        return_value=0,
        autospec=True,
    ) as mock:
        yield mock


#########
# TESTS #
#########


@travel("2023-12-01")
@pytest.mark.django_db
def test_overdue_members_sends_mail_without_error(
    mix_of_paid_and_overdue_members,
    mock_send_mail_in_command,
):
    members = Member.objects.dues_payment_pending()
    result = send_overdue_payment_mail(DEFAULT_TEMPLATE, DEFAULT_DOMAIN)
    mock_send_mail_in_command.assert_has_calls(
        [
            call(
                "A Notification Concerning Your AHS Membership Renewal",
                f"\n  {m.first_name} {m.last_name},\n\n  Greetings! Your annual membership payment for the American Handel Society is overdue.\n\n  Please login to the AHS website and complete the renewal form:\n\n  https://www.americanhandelsociety.org/\n\n  We apologize if you received this email in error. Do not reply directly; please email our web developer (reginafcompton@gmail.com) with issues.\n\n  Kind regards,\n  American Handel Society\n\n",
                ANY,
                [m.email],
                fail_silently=False,
            )
            for m in members
        ]
    )
    assert len(result) == 0


@travel(f"{year_now()}-12-01")
@pytest.mark.django_db
def test_exception_handling_for_overdue_payment_email(
    mix_of_paid_and_overdue_members,
    mock_send_mail_in_command,
):
    mock_send_mail_in_command.side_effect = [SMTPException("Email delivery failure!")]
    members = Member.objects.dues_payment_pending()
    result = send_overdue_payment_mail(members, DEFAULT_TEMPLATE, DEFAULT_DOMAIN)
    mock_send_mail_in_command.assert_has_calls(
        [
            call(
                "A Notification Concerning Your AHS Membership Renewal",
                f"\n  {m.first_name} {m.last_name},\n\n  Greetings! Your annual membership payment for the American Handel Society is overdue.\n\n  Please login to the AHS website and complete the renewal form:\n\n  https://www.americanhandelsociety.org/\n\n  We apologize if you received this email in error. Do not reply directly; please email our web developer (reginafcompton@gmail.com) with issues.\n\n  Kind regards,\n  American Handel Society\n\n",
                ANY,
                [m.email],
                fail_silently=False,
            )
            for m in members
        ]
    )
    assert len(result) == 5


@pytest.mark.django_db
def test_management_command_sends_on_appropriate_date(
    mix_of_paid_and_overdue_members,
    mock_send_mail_in_command,
):
    # command handler uses the same query. if the command handler changes
    # this test may fail, or worse, mysteriously pass
    members = Member.objects.dues_payment_pending()
    command = Command()
    with travel("1685-02-23"):
        command.send_overdue_payment_mail()
        mock_send_mail_in_command.assert_not_called()
    with travel(f"{year_now()}-03-01"):
        # Time warp
        command.send_overdue_payment_mail()
        mock_send_mail_in_command.assert_has_calls(
            [
                call(
                    "A Notification Concerning Your AHS Membership Renewal",
                    f"\n  {m.first_name} {m.last_name},\n\n  Greetings! Your annual membership payment for the American Handel Society is overdue.\n\n  Please login to the AHS website and complete the renewal form:\n\n  https://www.americanhandelsociety.org/\n\n  We apologize if you received this email in error. Do not reply directly; please email our web developer (reginafcompton@gmail.com) with issues.\n\n  Kind regards,\n  American Handel Society\n\n",
                    ANY,
                    [m.email],
                    fail_silently=False,
                )
                for m in members
            ]
        )


@travel("1985-01-01")
@pytest.mark.django_db
def test_management_command_skips_skippable_months_but_logs_on_first(
    mix_of_paid_and_overdue_members,
    mock_send_and_log,
    mock_email_command_logger,
):
    command = Command()
    command.send_overdue_payment_mail()
    mock_send_and_log.assert_not_called()
    mock_email_command_logger.info.assert_has_calls(
        [call("Is January: intentionally skipping e-mail sending this month.")]
    )


@travel("1985-01-07")
@pytest.mark.django_db
def test_management_command_skips_skippable_months_but_doesnt_log_on_other_days(
    mix_of_paid_and_overdue_members,
    mock_send_and_log,
    mock_email_command_logger,
):
    command = Command()
    command.send_overdue_payment_mail()
    mock_send_and_log.assert_not_called()
    mock_email_command_logger.info.assert_not_called()


@travel("2024-12-01")
@pytest.mark.django_db
def test_management_command_final_notice(
    mix_of_paid_and_overdue_members,
    mock_send_mail_in_command,
):
    # command handler uses the same query. if the command handler changes
    # this test may fail, or worse, mysteriously pass
    members = Member.objects.dues_payment_pending()
    command = Command()
    command.send_overdue_payment_mail()
    year = year_now()
    mock_send_mail_in_command.assert_has_calls(
        [
            call(
                "Final Notice: A Notification Concerning Your AHS Membership Renewal",
                f"\n  {m.first_name} {m.last_name},\n\n  Greetings! Your annual membership payment for the American Handel Society is overdue.\n\n  Your membership in the American Handel Society will be deactivated in {year + 1} if you do not submit your annual payment before the final day of {year}.\n\n  Please login to the AHS website and complete the renewal form:\n\n  https://www.americanhandelsociety.org/\n\n  Kind regards,\n  American Handel Society\n\n",
                ANY,
                [m.email],
                fail_silently=False,
            )
            for m in members
        ]
    )
