from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from time_machine import travel
from rest_framework.authtoken.models import Token

from americanhandelsociety_app.models import Member


def test_returns_401_if_user_is_not_authenticated(client):
    resp = client.post(f"/membership-renewal-webhook/", data={})
    assert resp.status_code == 401


@pytest.mark.django_db
def test_returns_401_if_user_is_not_an_admin(client, member):
    token, _ = Token.objects.get_or_create(user=member)
    resp = client.post(
        f"/membership-renewal-webhook/",
        data={},
        headers={"HTTP_AUTHORIZATION": f"Token {token.key}"},
    )
    assert resp.status_code == 401


@pytest.mark.django_db
def test_returns_400_if_payload_omits_email(client, member, auth_headers):
    data = {
        "membership_type": "AHS Regular",
        "first_name": member.first_name,
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data, **auth_headers)

    assert resp.status_code == 400
    assert resp.json() == {"email": ["This field is required."]}


@pytest.mark.django_db
def test_returns_400_if_payload_omits_membership_type(client, member, auth_headers):
    data = {
        "email": member.email,
        "first_name": member.first_name,
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data, **auth_headers)

    assert resp.status_code == 400
    assert resp.json() == {"membership_type": ["This field is required."]}


@pytest.mark.django_db
def test_returns_400_if_payload_omits_first_name(client, member, auth_headers):
    data = {
        "email": member.email,
        "membership_type": "Regular",
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data, **auth_headers)

    assert resp.status_code == 400
    assert resp.json() == {"first_name": ["This field is required."]}


@pytest.mark.django_db
def test_returns_400_if_payload_omits_last_name(client, member, auth_headers):
    data = {
        "email": member.email,
        "membership_type": "Regular",
        "first_name": member.first_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data, **auth_headers)

    assert resp.status_code == 400
    assert resp.json() == {"last_name": ["This field is required."]}


@pytest.mark.django_db
def test_returns_400_if_membership_type_is_not_valid(client, member, auth_headers):
    bad_type = "INVALID"
    data = {
        "email": member.email,
        "membership_type": bad_type,
        "first_name": member.first_name,
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data, **auth_headers)

    assert resp.status_code == 400
    assert resp.json() == {"membership_type": [f'"{bad_type}" is not a valid choice.']}


@pytest.mark.django_db
def test_returns_400_if_email_does_not_match_existing_record(
    client, member, auth_headers
):
    bad_email = "user@test.com"
    data = {
        "email": bad_email,
        "membership_type": "Regular",
        "first_name": member.first_name,
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data, **auth_headers)

    assert resp.status_code == 400
    assert resp.json() == {
        "error": {
            "message": f"ObjectDoesNotExist: Cannot find a Member with email '{bad_email}'"
        }
    }


@travel(datetime(2024, 1, 1, 0, 0, tzinfo=ZoneInfo("America/New_York")))
@pytest.mark.django_db
def test_success(client, member, auth_headers, subtests):
    data = {
        "email": member.email,
        "membership_type": "Cleopatra Circle",
        "first_name": member.first_name,
        "last_name": member.last_name,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data, **auth_headers)

    with subtests.test("returns 'ok' response"):
        assert resp.status_code == 200
        assert all(
            key in resp.json().keys()
            for key in ("member_email", "date_of_last_membership_payment", "is_active")
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


@pytest.mark.django_db
def test_uses_ahs_confirmed_email_for_lookup(client, member, auth_headers):
    data = {
        "email": "something.for.payment@test.com",
        "membership_type": "Cleopatra Circle",
        "first_name": member.first_name,
        "last_name": member.last_name,
        "confirmed_member_email": member.email,
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data, **auth_headers)

    assert resp.status_code == 200
    assert resp.json()["member_email"] == member.email
