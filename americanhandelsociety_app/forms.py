from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm
from captcha.fields import CaptchaField

from .models import Member, Address


class MemberCreationForm(UserCreationForm):
    captcha = CaptchaField(
        error_messages=dict(invalid="Invalid captcha. Please try again.")
    )

    class Meta:
        model = Member
        fields = ("first_name", "last_name", "email", "password1", "password2")


class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "institution",
            "available_in_directory",
        )


class AddressChangeForm(ModelForm):
    street_address = forms.CharField(required=False)
    street_address_2 = forms.CharField(required=False)
    street_address_3 = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state_province_region = forms.CharField(required=False)
    zip_postal_code = forms.CharField(required=False)
    country = forms.CharField(required=False)

    class Meta:
        model = Address
        fields = "__all__"
