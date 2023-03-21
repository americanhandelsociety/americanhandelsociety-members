from unittest.mock import patch
from smtplib import SMTPException

import pytest

from americanhandelsociety_app.management.commands.send_overdue_payment_email import (
    get_members_with_overdue_payments,
    send_overdue_payment_mail,
    Command,
)
from americanhandelsociety_app.models import Member
from americanhandelsociety_app.utils import year_now


###########
# PATCHES #
###########

# Most of the pytest fixtures can be found in
# tests/conftest.py. However, these fixtures are
# dependent on patch paths relevant to the tests
# in this particular file, thus these fixtures here.
@pytest.fixture
def mock_send_mail_in_command():
    with patch(
        "americanhandelsociety_app.management.commands.send_overdue_payment_email.send_mail",
        return_value=0,
        autospec=True,
    ) as mock:
        yield mock


@pytest.fixture
def mock_today_is_first_in_command():
    with patch(
        "americanhandelsociety_app.management.commands.send_overdue_payment_email.today_is_first_of_month",
        return_value=0,
        autospec=True,
    ) as mock:
        yield mock


#########
# TESTS #
#########


@pytest.mark.django_db
def test_overdue_members_correctly_filter(mix_of_paid_and_overdue_members):
    # This test relies on the configuration of dates and members
    # in the pytest fixture passed in the function header. If that
    # configuration changes, then this test might fail.
    year = year_now()
    members = get_members_with_overdue_payments()
    assert all(
        [m.membership_type != Member.MembershipType.MESSIAH_CIRCLE for m in members]
    ), f"Messiah Circle members cannot be overdue by definition."
    assert all(
        [m.date_of_last_membership_payment.year < year for m in members]
    ), "Member's payment year must be overdue to receive payment."
    assert all(
        [m.is_member_via_other_organization == False for m in members]
    ), "Members must have 'is_member_via_other_organization' set to False"
    assert len(members) == 7, f"Only expected 7 members with overdue payments."


@pytest.mark.django_db
def test_overdue_members_correctly_filter_and_sends_mail_without_error(
    mix_of_paid_and_overdue_members, mock_send_mail_in_command
):
    # This test relies on the configuration of dates and members
    # in the pytest fixture passed in the function header. If that
    # configuration changes, then this test might fail.
    members = get_members_with_overdue_payments()
    result = send_overdue_payment_mail(members)
    mock_send_mail_in_command.assert_called()
    assert len(result) == 0


@pytest.mark.django_db
def test_exception_handling_for_overdue_payment_email(
    mix_of_paid_and_overdue_members, mock_send_mail_in_command
):
    mock_send_mail_in_command.side_effect = [SMTPException("Email delivery failure!")]
    members = get_members_with_overdue_payments()
    result = send_overdue_payment_mail(members)
    mock_send_mail_in_command.assert_called()
    assert len(result) == 7


@pytest.mark.django_db
def test_management_command_sends_on_appropriate_date(
    mix_of_paid_and_overdue_members,
    mock_today_is_first_in_command,
    mock_send_mail_in_command,
):
    command = Command()
    mock_today_is_first_in_command.side_effect = [False, True]
    command.send_overdue_payment_mail()
    mock_send_mail_in_command.assert_not_called()
    # Time warp
    command.send_overdue_payment_mail()
    mock_send_mail_in_command.assert_called()
