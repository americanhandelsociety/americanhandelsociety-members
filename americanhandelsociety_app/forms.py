from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Member


class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ("first_name", "last_name", "email")
