from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

from .models import Member


class ProtectedView(LoginRequiredMixin):
    raise_exception = True


class MembersDirectory(ProtectedView, ListView):
    model = Member

    def get_template_names(self):
        return ["members_directory.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Profile(ProtectedView, View):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class Login(LoginView):
    template_name = "login.html"


class Logout(LogoutView):
    template_name = "logout.html"


# static views
class About(View):
    template_name = "about.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class People(View):
    template_name = "people.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)