import pytest

from americanhandelsociety_app.models import Member
from americanhandelsociety_app.forms import MemberCreationForm
from tests.utils import extract_hash_and_response, post_valid_user


@pytest.mark.django_db
def test_join_creates_user(client):
    resp = post_valid_user(client)

    assert resp.status_code == 302
    Member.objects.get(last_name="Cleopatra")


@pytest.mark.django_db
def test_join_does_not_set_user_to_active(client):
    resp = post_valid_user(client)

    assert resp.status_code == 302

    new_member = Member.objects.get(last_name="Cleopatra")
    assert not new_member.is_active


@pytest.mark.django_db
def test_join_fails_with_invalid_captcha(client):
    response = client.get("/join/")
    hash, _ = extract_hash_and_response(response)

    data = {
        "first_name": "Queen",
        "last_name": "Cleopatra",
        "email": "cleo@egypt.ico",
        "password1": "1724handel",
        "password2": "1724handel",
        "captcha_0": hash,
        "captcha_1": "the wrong answer",
    }

    response = client.post("/join/", data=data)
    expected_error_msg = MemberCreationForm.base_fields["captcha"].error_messages[
        "invalid"
    ]

    assert expected_error_msg in str(response.content)
