from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import Member, Address


class MemberCreationForm(UserCreationForm):
    captcha = CaptchaField(
        error_messages=dict(invalid="Invalid captcha. Please try again.")
    )
    email = forms.CharField(
        validators=[EmailValidator(message="Please enter a valid email address.")]
    )

    PRIVACY_POLICY_VALIDATION_MSG = "You must acknowledge receipt of the Privacy Policy to become a member of the American Handel Society."

    def clean_accepts_privacy_policy(self):
        value = self.cleaned_data.get("accepts_privacy_policy", False)

        if value:
            return value

        raise ValidationError(self.PRIVACY_POLICY_VALIDATION_MSG)

    class Meta:
        model = Member
        fields = (
            "first_name",
            "last_name",
            "email",
            "contact_preference",
            "password1",
            "password2",
            "accepts_privacy_policy",
        )


class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "institution",
            "contact_preference",
            "available_in_directory",
            "can_showcase_membership_or_donation_data",
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
