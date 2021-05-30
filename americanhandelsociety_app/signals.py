from django.conf import settings

from paypal.standard.models import ST_PP_COMPLETED

from .models import Member


def listen_for_paypal_please(sender, **kwargs):    
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

    payment_membership_map = {
        "35.00": "Regular",
        "42.00": "Joint",
        "56.00": "Donor",
        "20.00": "Student",
        "20.00": "Retired",
        "100.00": "Sponsor",
        "200.00": "Patron",
        "500.00": "Life",
        "42.00": "Subscriber",
    }

    member_uuid = ipn_obj.invoice.replace("_join", "")
    member = Member.objects.get(id=member_uuid)
    member.is_active = True
    member.save()

    print("Successful payment! Member updated.")

    # TODO: Set membership type
