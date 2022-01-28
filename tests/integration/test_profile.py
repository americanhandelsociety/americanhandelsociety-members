from datetime import datetime, timezone
from americanhandelsociety_app.models import Member

import pytest
from dateutil.relativedelta import relativedelta
from django.conf import settings


@pytest.mark.django_db
def test_profile_as_protected_view(client, member):
    # without user authentication
    resp = client.get("/profile/")
    assert resp.status_code == 403

    # with user authentication
    client.force_login(member)
    resp = client.get("/profile/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_profile_shows_user_info(client, member):
    client.force_login(member)

    resp = client.get("/profile/")

    assert member.first_name in resp.content.decode("utf-8")
    assert member.last_name in resp.content.decode("utf-8")
    assert member.email in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_profile_shows_address_info(client, member):
    client.force_login(member)

    resp = client.get("/profile/")

    assert "Mailing Address" in resp.content.decode("utf-8")
    assert member.address.street_address in resp.content.decode("utf-8")
    assert member.address.city in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_profile_hides_address_info_when_member_has_no_address(client, member):
    member.address = None
    member.save()

    client.force_login(member)

    resp = client.get("/profile/")

    assert "Mailing Address" not in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_profile_shows_user_directory_preference(
    client, member, member_not_in_directory
):
    client.force_login(member)
    resp = client.get("/profile/")
    assert (
        "Members of the AHS can view your information in the online Members Directory."
        in resp.content.decode("utf-8")
    )

    client.force_login(member_not_in_directory)
    resp = client.get("/profile/")
    assert (
        "Members of the AHS cannot view your information in the online Members Directory."
        in resp.content.decode("utf-8")
    )


@pytest.mark.skip("Skip. Datetime does not work as expected. May need mocks.")
@pytest.mark.django_db
def test_profile_shows_member_info(client, member):
    client.force_login(member)
    resp = client.get("/profile/")

    assert member.date_of_last_membership_payment.strftime(
        settings.DATE_FORMAT
    ) in resp.content.decode("utf-8")
    assert member.date_joined.strftime(settings.DATE_FORMAT) in resp.content.decode(
        "utf-8"
    )
    assert member.last_login.strftime(settings.DATETIME_FORMAT) in resp.content.decode(
        "utf-8"
    )


@pytest.mark.django_db
def test_profile_renewal_msg(client, member):
    # 'date_of_last_membership_payment' must be within 12 months of NOW, otherwise payment will be overdue
    not_overdue_timestamp = datetime.now(timezone.utc) - relativedelta(months=6)
    member.date_of_last_membership_payment = not_overdue_timestamp
    member.save()

    client.force_login(member)
    resp = client.get("/profile/")

    assert (
        "Renew your membership on or before this date to maintain membership benefits."
        in resp.content.decode("utf-8")
    )


@pytest.mark.django_db
def test_profile_renewal_msg_error(client, member):
    # 'date_of_last_membership_payment' must be within 12 months of NOW, otherwise payment will be overdue
    overdue_timestamp = datetime.now(timezone.utc) - relativedelta(months=13)
    member.date_of_last_membership_payment = overdue_timestamp
    member.save()

    client.force_login(member)
    resp = client.get("/profile/")

    assert "Membership payment overdue! Please renew today." in resp.content.decode(
        "utf-8"
    )


@pytest.mark.django_db
def test_profile_is_messiah_circle_member_is_true(client, member):
    member.membership_type = Member.MembershipType.MESSIAH_CIRCLE
    member.save()

    client.force_login(member)
    resp = client.get("/profile/")

    assert "<th>Renewal Date</th>" not in resp.content.decode("utf-8")
    assert "<th>Date of Last Membership Payment</th>" not in resp.content.decode(
        "utf-8"
    )
    assert "<th>Date Joined</th>" not in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_profile_is_messiah_circle_member_is_false(client, member):
    client.force_login(member)
    resp = client.get("/profile/")

    assert "<th>Renewal Date</th>" in resp.content.decode("utf-8")
    assert "<th>Date of Last Membership Payment</th>" in resp.content.decode("utf-8")
    assert "<th>Date Joined</th>" in resp.content.decode("utf-8")
