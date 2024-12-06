import pytest

from americanhandelsociety_app.templatetags.profile_extras import generate_renewal_url


@pytest.mark.django_db
def test_generate_renewal_url(member):
    assert (
        generate_renewal_url(member)
        == "https://www.zeffy.com/embed/ticketing/daa5a0a7-a8ff-4214-88eb-822fd0a78f8a?modal=true&email=rodelinda%40lombardy.sa&firstName=Queen&lastName=Rodelinda"
    )
