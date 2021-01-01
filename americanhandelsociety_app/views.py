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

from .models import Member

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
        # data = {"change_password_success": False}

        # print(kwargs, "!!!")
        # if "form-name" in kwargs and :
        #     data["change_password_success"] = True

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
