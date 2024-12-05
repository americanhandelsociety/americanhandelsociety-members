from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from time_machine import travel

from americanhandelsociety_app.models import Member


# Re-add test when doing
# def test_returns_403_if_user_is_not_authenticated(client):
#     resp = client.post(f"/membership-renewal-webhook/", data={})
#     assert resp.status_code == 403


@pytest.mark.django_db
def test_returns_400_if_payload_omits_email(client, member):
    data = {
        "membership_type": "Regular",
        "first_name": member.first_name,
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data)

    assert resp.status_code == 400
    assert resp.json() == {"email": "Required field."}


@pytest.mark.django_db
def test_returns_400_if_payload_omits_membership_type(client, member):
    data = {
        "email": member.email,
        "first_name": member.first_name,
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data)

    assert resp.status_code == 400
    assert resp.json() == {"membership_type": "Required field."}


@pytest.mark.django_db
def test_returns_400_if_payload_omits_first_name(client, member):
    data = {
        "email": member.email,
        "membership_type": "Regular",
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data)

    assert resp.status_code == 400
    assert resp.json() == {"first_name": "Required field."}


@pytest.mark.django_db
def test_returns_400_if_payload_omits_last_name(client, member):
    data = {
        "email": member.email,
        "membership_type": "Regular",
        "first_name": member.first_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data)

    assert resp.status_code == 400
    assert resp.json() == {"last_name": "Required field."}


@pytest.mark.django_db
def test_returns_400_if_email_does_not_match_existing_record(client, member):
    bad_email = "user@test.com"
    data = {
        "email": bad_email,
        "membership_type": "Regular",
        "first_name": member.first_name,
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data)

    assert resp.status_code == 400

    assert resp.json() == {
        "email": f"ObjectDoesNotExist: Cannot find a Member with email '{bad_email}'"
    }


@pytest.mark.django_db
def test_returns_400_if_membership_type_is_not_valid(client, member):
    bad_type = "INVALID"
    data = {
        "email": member.email,
        "membership_type": bad_type,
        "first_name": member.first_name,
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data)

    assert resp.status_code == 400
    assert resp.json() == {
        "error": {"message": [f"Value '{bad_type}' is not a valid choice."]}
    }


@travel(datetime(2024, 1, 1, 0, 0, tzinfo=ZoneInfo("America/New_York")))
@pytest.mark.django_db
def test_success(client, member, subtests):
    data = {
        "email": member.email,
        "membership_type": "Cleopatra Circle",
        "first_name": member.first_name,
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data)

    with subtests.test("returns 'ok' response"):
        assert resp.status_code == 200
        assert all(
            key in resp.json().keys()
            for key in ("email", "date_of_last_membership_payment", "is_active")
        )

    member.refresh_from_db()

    with subtests.test("sets Member.is_active to True"):
        assert member.is_active == True

    with subtests.test("assigns correct Member.membership_type"):
        assert member.membership_type == Member.MembershipType.CLEOPATRA_CIRCLE.value

    with subtests.test("updates Member renewal date"):
        assert (
            member.date_of_last_membership_payment.date()
            == datetime.strptime("2024-01-01", "%Y-%m-%d").date()
        )
