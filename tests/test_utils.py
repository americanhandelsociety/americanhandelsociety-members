from time_machine import travel

from americanhandelsociety_app.utils import (
    get_member_uuid_from_invoice,
    make_invoice_for_join,
    make_invoice_for_renew,
)

MEMBER_UUID = "ea96-40c9-8cd4"


def test_make_invoice_for_join():
    result = make_invoice_for_join(MEMBER_UUID)
    assert result == f"{MEMBER_UUID}_join"


# @travel("2012-11-01 00:00 +0000")
@travel("2012-11-01")
def test_make_invoice_for_renew():
    result = make_invoice_for_renew(MEMBER_UUID)
    assert result == f"{MEMBER_UUID}_renew_2012_11_01"


def test_get_member_uuid_from_invoice_for_join():
    invoice = make_invoice_for_join(MEMBER_UUID)
    result = get_member_uuid_from_invoice(invoice)
    assert result == MEMBER_UUID


def test_get_member_uuid_from_invoice_for_renew():
    invoice = make_invoice_for_renew(MEMBER_UUID)
    result = get_member_uuid_from_invoice(invoice)
    assert result == MEMBER_UUID
