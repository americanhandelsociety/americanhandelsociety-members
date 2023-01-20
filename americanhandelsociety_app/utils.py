import re
from datetime import datetime, timezone


def make_invoice_for_join(member_id: str):
    return f"{member_id}_join"


def make_invoice_for_renew(member_id: str):
    date = datetime.now().strftime("%Y_%m_%d")
    return f"{member_id}_renew_{date}"


def get_member_uuid_from_invoice(invoice: str):
    return re.sub("(_renew?.*)|(_join)", "", invoice)


def year_now():
    return datetime.now(timezone.utc).year


def today_is_first_of_month():
    return datetime.now(timezone.utc).day == 1
