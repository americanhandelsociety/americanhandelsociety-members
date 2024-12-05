import copy
import logging
from datetime import datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic.list import ListView
from americanhandelsociety_app.utils import (
    make_invoice_for_join,
    make_invoice_for_renew,
    year_now,
)
from paypal.standard.forms import PayPalPaymentsForm

from americanhandelsociety_app.newsletters import (
    MEMBERS_ONLY_NEWSLETTERS,
    NEWSLETTERS_DATA,
    PREVIEW_NEWSLETTERS,
)

from americanhandelsociety_app.constants import (
    BOARD_OF_DIRECTORS,
    BOSTON_25_AGENDA,
    HONORARY_DIRECTORS,
    HOWARD_SERWER_LECTURES,
    KNAPP_FELLOWSHIP_WINNERS,
    RESEARCH_MATERIALS,
)
from americanhandelsociety_app.forms import (
    AddressChangeForm,
    CircleMemberChangeForm,
    MemberChangeForm,
    MemberCreationForm,
)
from americanhandelsociety_app.models import Member


logger = logging.getLogger(__name__)


# views for authentication
class Login(LoginView):
    template_name = "forms/login.html"


class Logout(LogoutView):
    template_name = "logout.html"


# views that require (some) authorization
class ProtectedView(LoginRequiredMixin):
    raise_exception = True


class Profile(ProtectedView, View):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        is_messiah_circle_member = (
            request.user.membership_type == Member.MembershipType.MESSIAH_CIRCLE
        )
        year_of_last_membership_payment = (
            request.user.date_of_last_membership_payment.year
        )
        renewal_date = datetime(year_of_last_membership_payment + 1, 1, 1)

        if year_of_last_membership_payment < year_now():
            renewal_msg = "Your annual membership payment is due. Please renew today!"
            payment_overdue = True
        else:
            payment_overdue = False
            renewal_msg = "No action required at this time! You can renew your membership on or after January 1. "

        try:
            form_name = request.session.pop("form_name")
        except KeyError:
            form_name = None

        return render(
            request,
            self.template_name,
            context={
                **kwargs,
                "form_name": form_name,
                "renewal_date": renewal_date,
                "payment_overdue": payment_overdue,
                "renewal_msg": renewal_msg,
                "is_messiah_circle_member": is_messiah_circle_member,
            },
        )


class PasswordChange(PasswordChangeView, View):
    template_name = "forms/password_change.html"
    success_url = reverse_lazy("profile")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            request.session["form_name"] = "change-password-success"
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class EditMember(ProtectedView, View):
    template_name = "forms/edit_member.html"

    def get(self, request, member_uuid):
        member = Member.objects.get(id=member_uuid)

        # instantiate Member form; Circle members require an additional form field
        initial_form_data = {
            "first_name": member.first_name,
            "last_name": member.last_name,
            "email": member.email,
            "phone_number": member.phone_number,
            "contact_preference": member.contact_preference,
            "institution": member.institution,
        }
        if member.is_circle_member:
            form = CircleMemberChangeForm(
                initial={
                    **initial_form_data,
                    "publish_member_name_consent": member.publish_member_name_consent,
                },
                instance=member,
                use_required_attribute=False,
            )
        else:
            form = MemberChangeForm(
                initial=initial_form_data,
                instance=member,
                use_required_attribute=False,
            )

        # instantiate Address form
        address = member.address
        try:
            initial_data = {
                "street_address": address.street_address,
                "street_address_2": address.street_address_2,
                "street_address_3": address.street_address_3,
                "city": address.city,
                "state_province_region": address.state_province_region,
                "zip_postal_code": address.zip_postal_code,
                "country": address.country,
            }
        except AttributeError:
            initial_data = {}
        address_form = AddressChangeForm(initial=initial_data)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "address_form": address_form,
            },
        )

    def post(self, request, member_uuid):
        member = Member.objects.get(id=member_uuid)
        if member.is_circle_member:
            form = CircleMemberChangeForm(request.POST, instance=member)
        else:
            form = MemberChangeForm(request.POST, instance=member)
        address_form = AddressChangeForm(request.POST, instance=member.address)

        if form.is_valid() and address_form.is_valid():
            member = form.save(commit=False)
            address_form_data = [
                val for val in address_form.cleaned_data.values() if val
            ]
            if address_form_data:
                address = address_form.save()
                member.address = address
            else:
                address = member.address
                try:
                    address.delete()
                    member.address = None
                except AttributeError:
                    pass
            member.save()
            request.session["form_name"] = "change-member-info-success"
            success_url = reverse_lazy("profile")

            return HttpResponseRedirect(success_url)

        return render(
            request, self.template_name, {"form": form, "address_form": address_form}
        )


class Newsletter(View):
    template_name = "newsletter.html"

    def get(self, request):
        # # TECH DEBT: https://github.com/americanhandelsociety/americanhandelsociety-members/issues/77
        # from americanhandelsociety_app.newsletters import NewslettersData

        # print(
        #     NewslettersData(
        #         directory_path="newsletters/members_only"
        #     ).generate_newsletters_data()
        # )

        complete_newsletters_data = copy.deepcopy(NEWSLETTERS_DATA)
        if request.user.is_authenticated:
            complete_newsletters_data[:0] = MEMBERS_ONLY_NEWSLETTERS
        else:
            complete_newsletters_data[:0] = PREVIEW_NEWSLETTERS

        return render(
            request, self.template_name, {"newsletters_data": complete_newsletters_data}
        )


class People(ListView):
    context_object_name = "ahs_members"
    queryset = Member.objects.exclude(available_in_directory=False).order_by(
        "last_name"
    )

    def get_template_names(self):
        return ["people.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board_of_directors"] = BOARD_OF_DIRECTORS
        context["honorary_directors"] = HONORARY_DIRECTORS
        return context


class JoinOtherOrganizations(ProtectedView, View):
    template_name = "join_other_organizations.html"

    def get(self, request):
        return render(request, self.template_name)


# public-facing views with static content
class Home(View):
    template_name = "home.html"

    def get(self, request):
        images_content = [
            '"George Frideric Handel," photo by Thomas Hawk, licensed with Creative Commons BY-NC 2.0.',
            '"Happy we," <em>Acis and Galatea</em>, HWV 49, George Frideric Handel, 1715-32.',
            "Engraving by J. Faber the Younger, in Emma Marshall, <em>The Master of the Musicians</em>, Seeley & Co. 1896.",
            '"Berenstadt, Cuzzoni and Senesino," attributed to John Vanderbank, 1723, The British Museum, London.',
            '"Tu fedel? tu costante?," HWV 171a, George Frideric Handel, 1705-6.',
            '"align-justify," favicon by Fontawesome, licensed by <a target="_blank" href="https://fontawesome.com/license">Fontawesome</a>.',
        ]
        return render(request, self.template_name, {"images_content": images_content})


class Events(View):
    template_name = "events.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "howard_serwer_lectures": HOWARD_SERWER_LECTURES,
            },
        )


class Conference(View):
    template_name = "conference.html"

    def get(self, request):
        images_content = [
            '"George Frideric Handel," by Thomas Hudson, Public domain, via Wikimedia Commons.',
        ]

        print(BOSTON_25_AGENDA, "BOSTON_25_AGENDA")
        return render(
            request,
            self.template_name,
            {"images_content": images_content, "conference_agenda": BOSTON_25_AGENDA},
        )


class Awards(View):
    template_name = "awards.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {"knapp_fellowship_winners": KNAPP_FELLOWSHIP_WINNERS},
        )


class ResearchMaterials(View):
    template_name = "research_materials.html"

    def get(self, request):
        return render(
            request, self.template_name, {"research_materials": RESEARCH_MATERIALS}
        )


class Donate(View):
    template_name = "donate.html"

    def get(self, request):
        images_content = [
            '"Deeds of kindness," <em>Theodora</em>, HWV 68, British Library, R.M.20.f.9.'
        ]
        return render(request, self.template_name, {"images_content": images_content})


class Join(View):
    template_name = "forms/join.html"

    def get(self, request):
        form = MemberCreationForm(use_required_attribute=False)

        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = MemberCreationForm(request.POST)

        if form.is_valid():
            member = form.save(commit=False)
            member.is_active = False
            member.save()

            success_url = reverse_lazy("pay")

            request.session["member_id"] = str(member.id)

            logger.info(
                f"Someone clicked 'Continue' on the 'Join' form! member_id starts with: {str(member.id)[0:8]}"
            )

            return HttpResponseRedirect(success_url)

        return render(request, self.template_name, {"form": form})


class Pay(View):
    template_name = "forms/pay.html"

    def get(self, request, *args, **kwargs):
        member_id = request.session.get("member_id")
        invoice_num = make_invoice_for_join(member_id)
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "0",
            "item_name": "REGULAR",  # default to REGULAR membership type
            "invoice": invoice_num,
            "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
            "return": request.build_absolute_uri(
                reverse("pay-confirm")
            ),  # The URL to which PayPal redirects buyers' browser after they complete their payments.
            # TODO: How will we deal with cancelled payments?
            # "cancel_return": request.build_absolute_uri(reverse("your-cancel-view")),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {
            "form": form,
            "member_id": member_id,
            "membership_types": Member.MembershipType,
            "PAYPAL_ACTION_URL": settings.PAYPAL_ACTION_URL,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        member_id = request.session.get("member_id")
        try:
            member = Member.objects.get(id=member_id)
            member.delete()
        except Member.DoesNotExist:
            pass

        logger.info(
            f"Someone hit 'Cancel' on the 'Pay' page. member_id starts with: {str(member_id)[0:8]}"
        )

        return HttpResponseRedirect(reverse_lazy("join"))


class Renew(ProtectedView, View):
    template_name = "forms/renew.html"

    def get(self, request):
        member = request.user
        invoice_num = make_invoice_for_renew(member.id)
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "0",
            "item_name": member.membership_type,  # default to user's current membership type
            "invoice": invoice_num,
            "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
            "return": request.build_absolute_uri(
                reverse("renew-confirm")
            ),  # The URL to which PayPal redirects buyers' browser after they complete their payments.
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {
            "form": form,
            "member_id": member.id,
            "membership_types": Member.MembershipType,
            "PAYPAL_ACTION_URL": settings.PAYPAL_ACTION_URL,
        }

        return render(request, self.template_name, context)


class PaymentConfirmation(View):
    template_name = "payment_confirmation.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(PaymentConfirmation, self).dispatch(*args, **kwargs)


class PrivacyPolicy(View):
    template_name = "privacy_policy.html"

    def get(self, request):
        return render(request, self.template_name)


class RenewalConfirmation(ProtectedView, View):
    template_name = "renewal_confirmation.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# Custom Error Views


def page_not_found(request, *args, **kwargs):
    """Serve an AHS custom 404 page."""
    return render(request, "404.html", status=404)
