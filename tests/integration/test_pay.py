import pytest

from americanhandelsociety_app.models import Member


@pytest.mark.django_db
def test_can_cancel_join_and_remove_member_entity(client):
    # POST new member and assert its existence (based on data in 'request.session')
    data = {
        "first_name": "Queen",
        "last_name": "Cleopatra",
        "email": "cleo@egypt.ico",
        "password1": "1724handel",
        "password2": "1724handel",
    }
    client.post(f"/join/", data=data)
    member_id = client.session["member_id"]
    Member.objects.get(id=member_id)

    # POST to cancel join flow and assert that the member no longer exists
    resp = client.post(f"/pay/")
    assert resp.status_code == 302
    with pytest.raises(Member.DoesNotExist):
        Member.objects.get(id=member_id)


@pytest.mark.django_db
def test_can_cancel_join_without_error(client):
    # POST to the 'pay' view, even when a member does not exist in session state.
    resp = client.post(f"/pay/")
    assert resp.status_code == 302
