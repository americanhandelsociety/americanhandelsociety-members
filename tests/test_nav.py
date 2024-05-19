import pytest


def test_nav_renders_login_link_when_user_is_not_authenticated(client):
    login_a_tag = '<a class="nav-link" href="/login/"><i class="fas fa-sign-in-alt"></i> Login</a>'

    resp = client.get("/login/")

    assert resp.status_code == 200
    assert login_a_tag in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_nav_renders_logout_link_when_user_is_authenticated(client, member):
    logout_a_tag = '<a class="nav-link" href="/logout/"><i class="fas fa-sign-out-alt"></i> Logout</a>'

    client.force_login(member)
    resp = client.get("/people/")
    assert resp.status_code == 200
    assert logout_a_tag in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_nav_renders_other_organizations_link_when_user_is_authenticated(
    client, member
):
    client.force_login(member)
    resp = client.get("/join-other-organizations/")
    assert resp.status_code == 200
    assert "Join other organizations" in resp.content.decode("utf-8")
