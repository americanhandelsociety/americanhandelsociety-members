import pytest

from americanhandelsociety_app.models import Member
from americanhandelsociety_app.forms import MemberCreationForm
from tests.utils import extract_hash_and_response, make_valid_user_data, post_valid_user


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
    data = make_valid_user_data(client)
    data["captcha_1"] = "the wrong answer"

    response = client.post("/join/", data=data)
    expected_error_msg = MemberCreationForm.base_fields["captcha"].error_messages[
        "invalid"
    ]

    assert expected_error_msg in str(response.content)


@pytest.mark.django_db
def test_join_fails_when_user_does_not_accept_privacy_policy(client):
    data = make_valid_user_data(client)
    data["accepts_privacy_policy"] = False

    response = client.post("/join/", data=data)

    assert MemberCreationForm.PRIVACY_POLICY_VALIDATION_MSG in str(response.content)


@pytest.mark.django_db
def test_join_fails_when_user_enters_invalid_email(client):
    data = make_valid_user_data(client)
    data["email"] = "gobbledygook"

    response = client.post("/join/", data=data)

    assert "Please enter a valid email address." in str(response.content)
