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
from django.utils import timezone

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
        is_superuser = "Yes" if request.user.is_superuser else "No"

        return render(
            request,
            self.template_name,
            context={
                **kwargs,
                "is_superuser": is_superuser,
            },
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

            success_url = reverse_lazy(
                "success", kwargs={"form_name": "change-member-info-success"}
            )

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
