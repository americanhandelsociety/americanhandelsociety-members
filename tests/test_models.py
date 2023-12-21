import random
import string

from django.db.utils import DataError
from django.core.exceptions import ValidationError
import pytest

from americanhandelsociety_app.models import Address, Member
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
        contact_preference="EMAIL",
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
    members = Member.objects.dues_payment_pending()
    year = year_now()
    assert all(
        [m.membership_type != Member.MembershipType.MESSIAH_CIRCLE for m in members]
    ), f"Messiah Circle members cannot be overdue by definition."
    assert all(
        [m.date_of_last_membership_payment.year == year - 1 for m in members]
    ), "Member's payment year must be overdue to receive payment."
    assert all(
        [m.is_member_via_other_organization == False for m in members]
    ), "Members must have 'is_member_via_other_organization' set to False"
    assert (
        len(members) == 5
    ), f"Only expected 5 members with overdue payments, got {len(members)}."


@pytest.mark.django_db
def test_model_dues_payment_status_admin_display_method(
    mix_of_paid_and_overdue_members,
):
    statuses = [
        member.dues_paid_current_calendar_year() for member in Member.objects.all()
    ]
    assert len(list(filter(lambda x: x == "Yes", statuses))) == 2
    assert len(list(filter(lambda x: x == "No", statuses))) == 9
    assert len(list(filter(lambda x: x == None, statuses))) == 4


@pytest.mark.django_db
def test_model_updated_past_month_model_class_admin_display_method(
    artificially_backdated_pre_004_migration_members, address
):
    assert all(
        not member.updated_past_month() for member in Member.objects.all()
    ), "Preconditions not met"
    random_member = random.choice(artificially_backdated_pre_004_migration_members)
    random_member.address = address
    random_member.save()
    assert (
        len(
            list(
                filter(
                    lambda member: member.updated_past_month() == "Yes",
                    Member.objects.all(),
                )
            )
        )
        == 1
    )


@pytest.mark.django_db
def test_model_membership_admin_display_method(members_of_all_types):
    # Mostly testing the formatting
    assert {
        "Regular",
        "Student",
        "Retired",
        "Joint",
        "Rinaldo Circle",
        "Cleopatra Circle",
        "Theodora Circle",
        "Messiah Circle",
    } == set(member.membership() for member in Member.objects.all())
