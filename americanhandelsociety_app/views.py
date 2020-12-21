from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

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
