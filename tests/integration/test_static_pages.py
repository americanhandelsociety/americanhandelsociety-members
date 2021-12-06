import pytest


@pytest.mark.django_db
def test_research_materials(client):
    resp = client.get("/research-materials/")

    assert resp.status_code == 200


@pytest.mark.django_db
def test_hides_join_other_organizations_when_user_not_authenticated(client):
    resp = client.get("/join-other-organizations/")

    assert resp.status_code == 403


@pytest.mark.django_db
def test_members_directory_shows_member_info(client, member):
    client.force_login(member)
    resp = client.get("/join-other-organizations/")

    assert resp.status_code == 200
    assert "Join Other Organizations" in resp.content.decode("utf-8")
