import pytest

from americanhandelsociety_app.models import Member


@pytest.mark.django_db
def test_join_does_not_set_user_to_active(client):
    data = {
        "first_name": "Queen",
        "last_name": "Cleopatra",
        "email": "cleo@egypt.ico",
        "password1": "1724handel",
        "password2": "1724handel",
    }
    resp = client.post(f"/join/", data=data)

    assert resp.status_code == 302

    new_member = Member.objects.get(last_name="Cleopatra")
    assert not new_member.is_active
