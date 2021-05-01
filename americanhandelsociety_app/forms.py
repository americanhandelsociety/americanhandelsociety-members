from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import Member, Address


class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ("first_name", "last_name", "email")


class AddressChangeForm(ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
