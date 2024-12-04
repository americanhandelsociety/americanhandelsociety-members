import pytest


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
