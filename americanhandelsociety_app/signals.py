import logging

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED

from .models import Member

logger = logging.getLogger(__name__)


def listen_for_paypal_please(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status != ST_PP_COMPLETED:
        logger.error(f"Payment not complete. Invoice: {ipn_obj.invoice}")
        return

    # WARNING! Check that the receiver email is the same we previously
    # set on the `business` field. (The user could tamper with
    # that fields on the payment form before it goes to PayPal)
    if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
        logger.error(
            f"The receiver does not match the PAYPAL_RECEIVER_EMAIL in settings. Not a valid payment! Possible data tampering! Invoice: {ipn_obj.invoice}"
        )
        return

    if ipn_obj.mc_currency != "USD":
        logger.error(
            f"Currency mismatch. Not a valid payment! Invoice: {ipn_obj.invoice}"
        )
        return

    member_uuid = ipn_obj.invoice.replace("_join", "")

    try:
        member = Member.objects.get(id=member_uuid)
    except ObjectDoesNotExist:
        logger.error(
            f"ObjectDoesNotExist – Cannot find a member with an id that starts with: {str(member_uuid)[0:8]}"
        )
        return

    member.is_active = True
    member.membership_type = ipn_obj.item_name

    # Run full_clean to validate membership_type choices.
    member.full_clean()
    member.save()

    logger.info(
        f"Successful payment! Welcome to our newest member of the Society. Member id starts with: {str(member_uuid)[0:8]}"
    )
