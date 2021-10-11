import random
import string

from django.db.utils import DataError
from django.core.exceptions import ValidationError
import pytest

from americanhandelsociety_app.models import Member


@pytest.mark.django_db
def test_custom_abstract_user():
    """Test that the Member employs 'email' as the username field."""
    new_member = Member.objects.create(
        email="rodelinda@lombardy.sa",
        password="cuzzoni",
        first_name="Queen",
        last_name="Rodelinda",
        membership_type="PATRON",
    )

    assert not new_member.username
    assert new_member.USERNAME_FIELD == "email"


@pytest.mark.django_db
def test_create_superuser():
    """Test that the custom `create_superuser` instantiates expected Member
    object."""
    new_superuser = Member.objects.create_superuser(
        email="rodelinda@lombardy.sa",
        password="cuzzoni",
        first_name="Queen",
        last_name="Rodelinda",
        membership_type="PATRON",
    )

    assert new_superuser.is_superuser == True
    assert new_superuser.is_staff == True


@pytest.mark.django_db
@pytest.mark.parametrize("choice", Member.MembershipType.choices)
def test_membership_type_accepts_valid_choices(choice):
    new_member = Member.objects.create(
        email="rodelinda@lombardy.sa",
        password="cuzzoni",
        first_name="Queen",
        last_name="Rodelinda",
        membership_type=choice[0],
    )

    assert new_member.membership_type == choice[0]


@pytest.mark.django_db
def test_membership_type_does_not_accept_choice_longer_than_max_length():
    max_length = Member.MembershipType.max_length()
    invalid_choice = "".join(random.choices(string.digits, k=(max_length + 1)))

    with pytest.raises(DataError) as exc:
        Member.objects.create(
            email="rodelinda@lombardy.sa",
            password="cuzzoni",
            first_name="Queen",
            last_name="Rodelinda",
            membership_type=invalid_choice,
        )

    assert "value too long for type character varying(10)" in str(exc.value)


@pytest.mark.django_db
def test_membership_type_does_not_accept_invalid_choice():
    expected_error_message = {
        "membership_type": ["Value 'INVALID' is not a valid choice."]
    }
    invalid_member = Member(
        email="rodelinda@lombardy.sa",
        password="cuzzoni",
        first_name="Queen",
        last_name="Rodelinda",
        membership_type="INVALID",
    )

    with pytest.raises(ValidationError) as exc:
        invalid_member.full_clean()

    assert exc.value.message_dict == expected_error_message
