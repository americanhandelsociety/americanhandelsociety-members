from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
)
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic.list import ListView
from paypal.standard.forms import PayPalPaymentsForm

from .constants import (
    RESEARCH_MATERIALS,
    BOARD_OF_DIRECTORS,
    HONORARY_DIRECTORS,
    HOWARD_SERWER_LECTURES,
)
from .forms import AddressChangeForm, MemberChangeForm, MemberCreationForm
from .models import Member


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
        date_of_last_membership_payment = request.user.date_of_last_membership_payment
        renewal_date = date_of_last_membership_payment + relativedelta(years=1)

        if renewal_date > datetime.now(timezone.utc):
            renewal_msg = "Renew your membership on or before this date to maintain membership benefits."
            payment_overdue = False
        else:
            renewal_msg = "Membership payment overdue! Please renew today."
            payment_overdue = True

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
        form = MemberChangeForm(
            initial={
                "first_name": member.first_name,
                "last_name": member.last_name,
                "email": member.email,
                "phone_number": member.phone_number,
                "contact_preference": member.contact_preference,
                "institution": member.institution,
            },
            instance=member,
            use_required_attribute=False,
        )

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
            request, self.template_name, {"form": form, "address_form": address_form}
        )

    def post(self, request, member_uuid):
        member = Member.objects.get(id=member_uuid)
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


class People(ListView):
    context_object_name = "ahs_members"
    queryset = Member.objects.exclude(available_in_directory=False)

    def get_template_names(self):
        return ["people.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board_of_directors"] = BOARD_OF_DIRECTORS
        context["honorary_directors"] = HONORARY_DIRECTORS
        return context


# public-facing views with static content
class Home(View):
    template_name = "home.html"

    def get(self, request):
        images_content = [
            '"Happy we," <em>Acis and Galatea</em>, HWV 49, George Frideric Handel, 1715-32.',
            '"George Frideric Handel," attributed to Balthasar Denner, 1726–8, The National Portrait Gallery, London.',
            '"Berenstadt, Cuzzoni and Senesino," attributed to John Vanderbank, 1723, The British Museum, London.',
            '"Tu fedel? tu costante?," HWV 171a, George Frideric Handel, 1705-6.',
        ]
        return render(request, self.template_name, {"images_content": images_content})


class Events(View):
    template_name = "events.html"

    def get(self, request):
        images_content = [
            "Letter from King George III to Mrs. Delaney, British Library, MS Mus. 1818."
        ]
        return render(
            request,
            self.template_name,
            {
                "howard_serwer_lectures": HOWARD_SERWER_LECTURES,
                "images_content": images_content,
            },
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

            return HttpResponseRedirect(success_url)

        return render(request, self.template_name, {"form": form})


class Pay(View):
    template_name = "forms/pay.html"

    def get(self, request, *args, **kwargs):
        # test buyer
        # username: americanhandelsociety-buyer@gmail.com
        # password: computer-man
        member_id = request.session.get("member_id")
        invoice_num = f"{member_id}_join"
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

        return HttpResponseRedirect(reverse_lazy("join"))


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
