import uuid

from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from paypal.standard.forms import PayPalPaymentsForm

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
    pass


class Join(View):
    template_name = "join.html"

    def get(self, request, *args, **kwargs):
        # TODO:
        # (1) How to show a stylized form with dropdown? https://github.com/spookylukey/django-paypal/blob/master/paypal/standard/forms.py
        # (2) How to redirect to a payment page where you can "Pay without a PayPal account"?

        invoice_num = str(uuid.uuid4())[:13]
        # What you want the button to do.
        paypal_dict = {
            "business": "reginafcompton@gmail.com",
            "amount": "35.00",
            "item_name": "Regular Membership",
            "invoice": invoice_num,
            "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
            "return": request.build_absolute_uri(
                reverse("login")
            ),  # The URL to which PayPal redirects buyers' browser after they complete their payments.
            "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
            # TODO: How will we deal with cancelled payments?
            # "cancel_return": request.build_absolute_uri(reverse("your-cancel-view")),
        }

        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form}
        return render(request, self.template_name, context)
