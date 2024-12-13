import pytest

from americanhandelsociety_app.templatetags.profile_extras import generate_renewal_url
from americanhandelsociety_app.constants import ZEFFY_EMBED_URL_FOR_RENEWAL_FORM


@pytest.mark.django_db
def test_generate_renewal_url(member):
    assert (
        generate_renewal_url(member)
        == f"{ZEFFY_EMBED_URL_FOR_RENEWAL_FORM}?modal=true&email=rodelinda%40lombardy.sa&firstName=Queen&lastName=Rodelinda"
    )
