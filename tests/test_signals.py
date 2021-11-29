import pytest
from django.conf import settings
from six import text_type
from six.moves.urllib.parse import urlencode

from americanhandelsociety_app.models import Member


CHARSET = "windows-1252"


@pytest.mark.skip("TODO – Fix. Does not work on Macbook 2015")
@pytest.mark.django_db
def test_listen_for_paypal_please_updates_member(client, member):
    """Assert that when app receives Pyapal signal, the member instance has the
    following: (1) 'is_active' is True, and (2) 'membership_type' is the
    'item_name' from the ipm params.

    Reference: https://github.com/spookylukey/django-paypal/blob/master/paypal/standard/ipn/tests/test_ipn.py
    """
    expected_membership_type = "PATRON"
    member.is_active = False
    member.membership_type = None
    member.full_clean()
    member.save()

    invoice = f"{member.id}_join"
    ipn_post_params = {
        "first_name": b"George",
        "last_name": b"Handel",
        "receiver_email": settings.PAYPAL_RECEIVER_EMAIL,
        "payment_status": b"Completed",
        "payment_gross": b"40.00",
        "invoice": bytes(invoice, encoding="utf-8"),
        "payer_status": b"verified",
        "item_name": bytes(expected_membership_type, encoding="utf-8"),
        "charset": CHARSET.encode("ascii"),
        "notify_version": b"2.6",
        "transaction_subject": b"",
        "test_ipn": b"1",
        "item_number": b"",
        "receiver_id": b"258DLEHY2BDK6",
        "payer_id": b"BN5JZ2V7MLEV4",
        "verify_sign": b"An5ns1Kso7MWUdW4ErQKJJJ4qi4-AqdZy6dD.sGO3sDhTf1wAbuO2IZ7",
        "mc_currency": b"USD",
        "payer_email": b"bishan_1233269544_per@gmail.com",
    }

    cond_encode = lambda v: v.encode(CHARSET) if isinstance(v, text_type) else v
    byte_params = {cond_encode(k): cond_encode(v) for k, v in ipn_post_params.items()}
    post_data = urlencode(byte_params)

    client.post("/paypal/", post_data, content_type="application/x-www-form-urlencoded")

    member = Member.objects.get(id=member.id)

    assert member.is_active == True
    assert member.membership_type == expected_membership_type
