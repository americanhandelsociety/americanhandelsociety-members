import pytest

from django.forms.models import model_to_dict

from americanhandelsociety_app.models import Address, Member


@pytest.mark.django_db
def test_updates_user_info(client, member):
    client.force_login(member)
    data = {**model_to_dict(member), "first_name": "Julia", "last_name": "Agrippina"}

    resp = client.post(f"/edit-member/{member.id}", data=data)
    assert resp.status_code == 302

    resp = client.get("/profile/")
    assert data["first_name"] in resp.content.decode("utf-8")
    assert data["last_name"] in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_updates_address_info_edit_existing(client, member):
    client.force_login(member)
    data = {
        **model_to_dict(member),
        "street_address": "Teatro La Fenice",
        "city": "Venice",
        "country": "Italy",
    }
    resp = client.post(f"/edit-member/{member.id}", data=data)
    assert resp.status_code == 302

    resp = client.get("/profile/")
    assert data["street_address"] in resp.content.decode("utf-8")
    assert data["city"] in resp.content.decode("utf-8")
    assert data["country"] in resp.content.decode("utf-8")

    address = Address.objects.get(
        street_address=data["street_address"],
        city=data["city"],
        country=data["country"],
    )
    assert address


@pytest.mark.django_db
def test_updates_address_info_remove_existing(client, member):
    client.force_login(member)
    resp = client.get(f"/edit-member/{member.id}")
    assert member.address.street_address in resp.content.decode("utf-8")

    resp = client.post(f"/edit-member/{member.id}", data=model_to_dict(member))
    assert resp.status_code == 302

    resp = client.get("/profile/")
    assert member.address.street_address not in resp.content.decode("utf-8")

    with pytest.raises(Address.DoesNotExist) as e_info:
        Address.objects.get(street_address=member.address.street_address)


@pytest.mark.django_db
def test_updates_address_info_create_new(client, member):
    client.force_login(member)

    member.address = None
    member.save()
    Address.objects.all().delete()

    data = {
        **model_to_dict(member),
        "address": "",
        "street_address": "Teatro La Fenice",
        "city": "Venice",
        "country": "Italy",
    }
    resp = client.post(f"/edit-member/{member.id}", data=data)
    assert resp.status_code == 302

    resp = client.get("/profile/")
    assert data["street_address"] in resp.content.decode("utf-8")
    assert data["city"] in resp.content.decode("utf-8")
    assert data["country"] in resp.content.decode("utf-8")

    address = Address.objects.get(
        street_address=data["street_address"],
        city=data["city"],
        country=data["country"],
    )
    assert address

    addresses = Address.objects.all()
    assert len(addresses) == 1


@pytest.mark.django_db
def test_update_available_in_directory(client, member):
    client.force_login(member)

    data = {**model_to_dict(member), "available_in_directory": False}
    resp = client.post(f"/edit-member/{member.id}", data=data)
    assert resp.status_code == 302

    resp = client.get("/profile/")
    assert (
        "Members of the AHS cannot view your information in the online Members Directory."
        in resp.content.decode("utf-8")
    )

    revise_data = {**data, "available_in_directory": True}
    resp = client.post(f"/edit-member/{member.id}", data=revise_data)
    assert resp.status_code == 302

    resp = client.get("/profile/")
    assert (
        "Members of the AHS can view your information in the online Members Directory."
        in resp.content.decode("utf-8")
    )


@pytest.mark.django_db
def test_update_contact_preference(client, member):
    client.force_login(member)

    data = {**model_to_dict(member), "contact_preference": "EMAIL"}
    resp = client.post(f"/edit-member/{member.id}", data=data)
    assert resp.status_code == 302

    resp = client.get("/profile/")
    assert (
        "You receive the AHS newsletter in <strong>EMAIL</strong> format."
        in resp.content.decode("utf-8")
    )

    revise_data = {**model_to_dict(member), "contact_preference": "PRINT"}
    resp = client.post(f"/edit-member/{member.id}", data=revise_data)
    assert resp.status_code == 302

    resp = client.get("/profile/")
    assert (
        "You receive the AHS newsletter in <strong>PRINT</strong> format."
        in resp.content.decode("utf-8")
    )


@pytest.mark.django_db
def test_update_phone_number(client, member):
    client.force_login(member)

    data = {**model_to_dict(member), "phone_number": "999-777-1111"}
    resp = client.post(f"/edit-member/{member.id}", data=data)
    assert resp.status_code == 302

    resp = client.get("/profile/")
    assert "999-777-1111" in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_update_institution(client, member):
    client.force_login(member)

    data = {**model_to_dict(member), "institution": "Eastman School of Music"}
    resp = client.post(f"/edit-member/{member.id}", data=data)
    assert resp.status_code == 302

    resp = client.get("/profile/")
    assert "Eastman School of Music" in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_does_not_render_publish_member_name_consent_field_for_regular_member(
    client, member
):
    client.force_login(member)
    resp = client.get(f"/edit-member/{member.id}")
    assert (
        "Rinaldo, Cleopatra, Theodora, and Messiah Circle members: do you consent to publishing your name and membership tier in the AHS newsletter and on the website?"
        not in resp.content.decode("utf-8")
    )


@pytest.mark.django_db
def test_renders_publish_member_name_consent_field_for_circle_member(
    client, circle_member
):
    client.force_login(circle_member)
    resp = client.get(f"/edit-member/{circle_member.id}")
    assert (
        "Rinaldo, Cleopatra, Theodora, and Messiah Circle members: do you consent to publishing your name and membership tier in the AHS newsletter and on the website?"
        in resp.content.decode("utf-8")
    )


@pytest.mark.django_db
def test_updates_publish_member_name_consent(client, circle_member):
    consent_text = "You granted permission to publish your name and membership tier."

    # arrange, and assert that the profile view does not render expected message
    client.force_login(circle_member)
    resp = client.get("/profile/")
    assert consent_text not in resp.content.decode("utf-8")

    # act
    data = {**model_to_dict(circle_member), "publish_member_name_consent": "YES"}
    resp = client.post(f"/edit-member/{circle_member.id}", data=data)
    assert resp.status_code == 302

    # assert
    resp = client.get("/profile/")
    assert consent_text in resp.content.decode("utf-8")
