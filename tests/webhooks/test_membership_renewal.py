from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from time_machine import travel

from americanhandelsociety_app.models import Member


def test_returns_400_if_payload_omits_member_uuid(client):
    data = {"membership_type": "Regular"}

    resp = client.post(f"/membership-renewal-webhook/", data=data)
    assert resp.status_code == 400
    assert resp.json() == {"member_uuid": "Required field."}


@pytest.mark.django_db
def test_returns_400_if_payload_omits_membership_type(client, member):
    data = {"member_uuid": member.id}

    resp = client.post(f"/membership-renewal-webhook/", data=data)
    assert resp.status_code == 400
    assert resp.json() == {"membership_type": "Required field."}


def test_returns_400_if_member_uuid_is_invalid(client):
    data = {"membership_type": "Regular", "member_uuid": 1234}

    resp = client.post(f"/membership-renewal-webhook/", data=data)
    assert resp.status_code == 400
    assert resp.json() == {"member_uuid": "Not a valid UUID."}


@pytest.mark.django_db
def test_returns_400_if_member_uuid_does_not_match_existing_record(client, member):
    data = {
        "membership_type": "Regular",
        "member_uuid": "cccccccc-4444-5555-bbbb-777777777777",
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data)
    assert resp.status_code == 400
    assert resp.json() == {
        "member_uuid": "ObjectDoesNotExist: Cannot find a Member with id 'cccccccc-4444-5555-bbbb-777777777777'"
    }


@pytest.mark.django_db
def test_returns_400_if_membership_type_is_not_valid(client, member):
    data = {
        "membership_type": "Invalid type",
        "member_uuid": str(member.id),
    }

    resp = client.post(f"/membership-renewal-webhook/", data=data)
    assert resp.status_code == 400
    assert resp.json() == {
        "error": {"message": ["Value 'Invalid type' is not a valid choice."]}
    }


@travel(datetime(2024, 1, 1, 0, 0, tzinfo=ZoneInfo("America/New_York")))
@pytest.mark.django_db
def test_success(client, member, subtests):
    member.is_active = False
    member.membership_type = Member.MembershipType.REGULAR.value
    member.save()

    data = {
        "membership_type": Member.MembershipType.CLEOPATRA_CIRCLE.value,
        "member_uuid": str(member.id),
    }
    resp = client.post(f"/membership-renewal-webhook/", data=data)

    with subtests.test("returns 'ok' response"):
        assert resp.status_code == 200
        assert all(
            key in resp.json().keys()
            for key in ("member_uuid", "date_of_last_membership_payment", "is_active")
        )

    with subtests.test("sets Member.is_active to True"):
        member.refresh_from_db()
        assert member.is_active == True

    with subtests.test("assigns correct Member.membership_type"):
        assert member.membership_type == Member.MembershipType.CLEOPATRA_CIRCLE.value

    with subtests.test("updates Member renewal date"):
        assert (
            member.date_of_last_membership_payment.date()
            == datetime.strptime("2024-01-01", "%Y-%m-%d").date()
        )
