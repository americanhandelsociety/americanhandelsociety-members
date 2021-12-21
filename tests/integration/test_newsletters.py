from americanhandelsociety_app.newsletters import (
    PREVIEW_NEWSLETTERS,
    MEMBERS_ONLY_NEWSLETTERS,
)
import pytest


@pytest.mark.django_db
def test_shows_previews_when_user_is_not_authenticated(client):
    resp = client.get("/newsletter/")

    assert resp.status_code == 200

    for el in PREVIEW_NEWSLETTERS:
        assert el["friendly_name"] in resp.content.decode("utf-8")
        assert el["filename"] in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_does_not_show_members_only_newsletters_when_user_is_not_authenticated(client):
    resp = client.get("/newsletter/")

    assert resp.status_code == 200

    for el in MEMBERS_ONLY_NEWSLETTERS:
        assert el["friendly_name"] not in resp.content.decode("utf-8")
        assert el["filename"] not in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_shows_members_only_newsletters_when_user_is_authenticated(client, member):
    client.force_login(member)
    resp = client.get("/newsletter/")

    assert resp.status_code == 200

    for el in MEMBERS_ONLY_NEWSLETTERS:
        assert el["friendly_name"] in resp.content.decode("utf-8")
        assert el["filename"] in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_does_not_show_previews_when_user_is_authenticated(client, member):
    client.force_login(member)
    resp = client.get("/newsletter/")

    assert resp.status_code == 200

    for el in PREVIEW_NEWSLETTERS:
        assert el["friendly_name"] not in resp.content.decode("utf-8")
        assert el["filename"] not in resp.content.decode("utf-8")
