import pytest


@pytest.mark.django_db
def test_members_directory_as_protected_view(client, member):
    # without user authentication
    resp = client.get("/members-directory/")
    assert resp.status_code == 403

    # with user authentication
    client.force_login(member)
    resp = client.get("/members-directory/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_members_directory_shows_member_info(client, member):
    client.force_login(member)

    resp = client.get("/members-directory/")

    assert member.email in resp.content.decode("utf-8")
