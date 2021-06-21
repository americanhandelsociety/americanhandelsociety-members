import pytest


@pytest.mark.django_db
def test_hides_members_when_user_not_authenticated(client, member):
    resp = client.get("/people/")

    assert resp.status_code == 200
    assert member.email not in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_members_directory_shows_member_info(client, member):
    client.force_login(member)
    resp = client.get("/people/")

    assert resp.status_code == 200
    assert member.email in resp.content.decode("utf-8")

@pytest.mark.django_db
def test_members_directory_hides_members_who_do_not_opt_in(client, member, member_not_in_directory):
    client.force_login(member)
    resp = client.get("/people/")

    assert resp.status_code == 200
    assert member_not_in_directory.email not in resp.content.decode("utf-8")
