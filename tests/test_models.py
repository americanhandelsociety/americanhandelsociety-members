import pytest

from americanhandelsociety_app.models import Member


@pytest.mark.django_db
def test_custom_abstract_user():
    """Test that the Member employs 'email' as the username field"""
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
    """Test that the custom `create_superuser` instantiates expected Member object"""
    new_superuser = Member.objects.create_superuser(
        email="rodelinda@lombardy.sa",
        password="cuzzoni",
        first_name="Queen",
        last_name="Rodelinda",
    )

    assert new_superuser.is_superuser == True
    assert new_superuser.is_staff == True
