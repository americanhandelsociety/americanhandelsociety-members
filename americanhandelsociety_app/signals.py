from django.conf import settings

from paypal.standard.models import ST_PP_COMPLETED

from .models import Member


def listen_for_paypal_please(sender, **kwargs):
    print("wheeee!!!!")

    ipn_obj = sender
    if ipn_obj.payment_status != ST_PP_COMPLETED:
        print("Payment not complete.")
        return

    # WARNING! Check that the receiver email is the same we previously
    # set on the `business` field. (The user could tamper with
    # that fields on the payment form before it goes to PayPal)
    if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
        print("Receiver email mismatch. Not a valid payment!")
        return

    if ipn_obj.mc_currency != "USD":
        print("Currency mismatch. Not a valid payment!")
        return

    member_uuid = ipn_obj.invoice.replace("_join", "")
    member = Member.objects.get(id=member_uuid)
    member.is_active = True
    member.membership_type = ipn_obj.item_name
    # Run full_clean to validate membership_type choices.
    member.full_clean()
    member.save()

    print("Successful payment! Member updated.")
