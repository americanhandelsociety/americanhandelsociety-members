from django.shortcuts import render
from django.urls import reverse_lazy
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

from .models import Member
from .forms import MemberChangeForm, AddressChangeForm

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
        return render(
            request,
            self.template_name,
            kwargs,
        )


class PasswordChange(PasswordChangeView, View):
    template_name = "password_change.html"
    success_url = reverse_lazy(
        "success", kwargs={"form_name": "change-password-success"}
    )


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

        address = member.address or {}

        address_form = AddressChangeForm(
            initial={
                "street_address": address.get("street_address"),
                "street_address_2": address.get("street_address_2"),
                "city": address.get("city"),
                "state_province_region": address.get("state_province_region"),
                "zip_postal_code": address.get("zip_postal_code"),
                "country": address.get("country"),
            }
        )

        return render(
            request, self.template_name, {"form": form, "address_form": address_form}
        )

    def post(self, request, member_uuid):
        member = Member.objects.get(id=member_uuid)
        form = MemberChangeForm(request.POST, instance=member)

        # FIXME!
        address_form = AddressChangeForm(request.POST, instance=member.address)

        if form.is_valid() and address_form.is_valid():
            form.save()
            address_form.save()
            success_url = reverse_lazy(
                "success", kwargs={"form_name": "change-member-info-success"}
            )

            return HttpResponseRedirect(success_url)


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
