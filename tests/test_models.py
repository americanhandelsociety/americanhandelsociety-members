import random
import string
from unittest.mock import ANY, patch

from django.db.utils import DataError
from django.conf import settings
from django.core.exceptions import ValidationError
import pytest

from americanhandelsociety_app.models import Address, Member
from americanhandelsociety_app.management.commands.send_overdue_payment_email import (
    get_members_with_overdue_payments,
    send_overdue_payment_mail,
)
from americanhandelsociety_app.utils import year_now


@pytest.mark.django_db
def test_custom_abstract_user():
    """Test that the Member employs 'email' as the username field."""
    new_member = Member.objects.create(
        email="rodelinda@lombardy.sa",
        password="cuzzoni",
        first_name="Queen",
        last_name="Rodelinda",
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

    assert "value too long for type character varying(16)" in str(exc.value)


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


@pytest.mark.django_db
def test_contact_preference_does_not_accept_choice_longer_than_max_length():
    max_length = Member.ContactPreference.max_length()
    invalid_choice = "".join(random.choices(string.digits, k=(max_length + 1)))

    with pytest.raises(DataError) as exc:
        Member.objects.create(
            email="rodelinda@lombardy.sa",
            password="cuzzoni",
            first_name="Queen",
            last_name="Rodelinda",
            contact_preference=invalid_choice,
        )

    assert "value too long for type character varying(5)" in str(exc.value)


@pytest.mark.django_db
def test_contact_preference_does_not_accept_invalid_choice():
    expected_error_message = {
        "contact_preference": ["Value 'INVALID' is not a valid choice."]
    }
    invalid_member = Member(
        email="rodelinda@lombardy.sa",
        password="cuzzoni",
        first_name="Queen",
        last_name="Rodelinda",
        contact_preference="INVALID",
    )

    with pytest.raises(ValidationError) as exc:
        invalid_member.full_clean()

    assert exc.value.message_dict == expected_error_message


@pytest.mark.django_db
def test_address_model_is_valid_with_street_address_only():
    street_address = "25 Brook Street"
    address = Address(street_address=street_address)

    assert address.street_address == street_address
    assert str(address) == street_address


@pytest.mark.django_db
def test_address_model_str_representation(address):
    assert (
        str(address)
        == "The Handel House Trust Ltd, 25 Brook Street, London, W1K 4HB, UK"
    )


@pytest.mark.django_db
def test_overdue_members_correctly_filter(mix_of_paid_and_overdue_members):
    # This test relies on the configuration of dates and members
    # in the pytest fixture passed in the function header. If that
    # configuration changes, then this test might fail.
    year = year_now()
    members = get_members_with_overdue_payments()
    assert all(
        [m.membership_type != Member.MembershipType.MESSIAH_CIRCLE for m in members]
    ), f"Messiah Circle members cannot be overdue by definition."
    assert all(
        [m.date_of_last_membership_payment.year < year for m in members]
    ), "Member's payment year must be overdue to receive payment."
    assert len(members) == 8, f"Only expected 8 members with overdue payments."


@pytest.mark.django_db
def test_overdue_members_correctly_filter(mix_of_paid_and_overdue_members):
    # This test relies on the configuration of dates and members
    # in the pytest fixture passed in the function header. If that
    # configuration changes, then this test might fail.
    year = year_now()
    with patch(
        "americanhandelsociety_app.management.commands.send_overdue_payment_email.send_mail"
    ) as mocked_send:
        members = get_members_with_overdue_payments()
        result = send_overdue_payment_mail(members)
        mocked_send.assert_called()
        assert len(result) == 0
