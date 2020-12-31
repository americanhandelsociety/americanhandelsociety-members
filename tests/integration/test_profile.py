import pytest


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
