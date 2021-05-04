import uuid

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.http import HttpResponseRedirect
from paypal.standard.forms import PayPalPaymentsForm

from .models import Member
from .forms import MemberCreationForm, MemberChangeForm, AddressChangeForm

# views for authentication
class Login(LoginView):
    template_name = "login.html"


class Logout(LogoutView):
    template_name = "logout.html"


# views that require (some) authorization
class ProtectedView(LoginRequiredMixin):
    raise_exception = True


class Profile(ProtectedView, View):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        is_superuser = "Yes" if request.user.is_superuser else "No"

        try:
            form_name = request.session.pop("form_name")
        except KeyError:
            form_name = None

        return render(
            request,
            self.template_name,
            context={**kwargs, "is_superuser": is_superuser, "form_name": form_name},
        )


class PasswordChange(PasswordChangeView, View):
    template_name = "password_change.html"
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
            },
            instance=member,
        )

        address = member.address

        try:
            initial_data = {
                "street_address": address.street_address,
                "street_address_2": address.street_address_2,
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
    model = Member

    def get_template_names(self):
        return ["people.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# public-facing views with static content
class About(View):
    template_name = "about.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class Join(View):
    template_name = "forms/join.html"

    def get(self, request):
        form = MemberCreationForm()

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
        # TODO: How to redirect to a payment page where you can "Pay without a PayPal account"?

        member_id = request.session.get("member_id")
        invoice_num = str(uuid.uuid4())[:13]
        paypal_dict = {
            "business": "reginafcompton@gmail.com",
            "amount": "0",
            "item_name": "Membership in the American Handel Society",
            "invoice": invoice_num,
            "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
            "return": request.build_absolute_uri(
                reverse("login")
            ),  # The URL to which PayPal redirects buyers' browser after they complete their payments.
            "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
            # TODO: How will we deal with cancelled payments?
            # "cancel_return": request.build_absolute_uri(reverse("your-cancel-view")),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form, "member_id": member_id}

        return render(request, self.template_name, context)
