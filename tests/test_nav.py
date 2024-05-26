import pytest


@pytest.mark.django_db
def test_nav_login_link(client, member, subtests):
    login_a_tag = '<a class="nav-link" href="/login/"><i class="fas fa-sign-in-alt"></i> Login</a>'

    with subtests.test("user is not authenticated"):
        resp = client.get("/")
        assert resp.status_code == 200
        assert login_a_tag in resp.content.decode("utf-8")

    with subtests.test("user is authenticated"):
        client.force_login(member)
        resp = client.get("/")
        assert resp.status_code == 200
        assert login_a_tag not in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_nav_profile_link(client, member, subtests):
    profile_a_tag = '<a class="dropdown-item" href="/profile/">'

    with subtests.test("user is not authenticated"):
        resp = client.get("/")
        assert resp.status_code == 200
        assert profile_a_tag not in resp.content.decode("utf-8")

    with subtests.test("user is authenticated"):
        client.force_login(member)
        resp = client.get("/")
        assert resp.status_code == 200
        assert profile_a_tag in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_nav_join_other_orgs_link(client, member, subtests):
    join_other_a_tag = '<a class="dropdown-item" href="/join-other-organizations/">'

    with subtests.test("user is not authenticated"):
        resp = client.get("/")
        assert resp.status_code == 200
        assert join_other_a_tag not in resp.content.decode("utf-8")

    with subtests.test("user is authenticated"):
        client.force_login(member)
        resp = client.get("/")
        assert resp.status_code == 200
        assert join_other_a_tag in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_nav_renew_link(client, member, subtests):
    renew_link = '<a class="dropdown-item" href="/renew/">'

    with subtests.test("user is not authenticated"):
        resp = client.get("/")
        assert resp.status_code == 200
        assert renew_link not in resp.content.decode("utf-8")

    with subtests.test("user is authenticated but does not have overdue membership"):
        client.force_login(member)
        resp = client.get("/")
        assert resp.status_code == 200
        assert renew_link not in resp.content.decode("utf-8")

    with subtests.test("user is authenticated and has overdue membership"):
        # arrange: set the date_of_last_membership_payment to a date in the past
        member.date_of_last_membership_payment = "2020-01-01"
        member.save()

        # act
        resp = client.get("/")

        # assert
        assert resp.status_code == 200
        assert renew_link in resp.content.decode("utf-8")
