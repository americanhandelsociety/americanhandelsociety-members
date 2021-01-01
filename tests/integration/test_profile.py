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
    assert member.email in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_profile_shows_user_directory_preference(
    client, member, member_not_in_directory
):
    client.force_login(member)
    resp = client.get("/profile/")
    assert (
        "Members of the AHS can view my information in the online Members Directory."
        in resp.content.decode("utf-8")
    )

    client.force_login(member_not_in_directory)
    resp = client.get("/profile/")
    assert (
        "Members of the AHS cannot view my information in the online Members Directory."
        in resp.content.decode("utf-8")
    )
