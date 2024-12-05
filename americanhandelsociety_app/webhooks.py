import logging
from datetime import datetime, timezone

from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin

from americanhandelsociety_app.models import Member


logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class MembershipRenewalWebhook(View):
    def _handle_error(self, error: dict, status_code: int = 400):
        logger.error(error)
        return JsonResponse(error, status=status_code)

    def _validate_required_field(self, field_name, value):
        if not value:
            raise ValidationError("Required field.", code=field_name)

        return value

    def post(self, request):
        try:
            email = self._validate_required_field(
                field_name="email", value=request.POST.get("email")
            )
            membership_type = self._validate_required_field(
                field_name="membership_type", value=request.POST.get("membership_type")
            )
            first_name = self._validate_required_field(
                field_name="first_name", value=request.POST.get("first_name")
            )
            last_name = self._validate_required_field(
                field_name="last_name", value=request.POST.get("last_name")
            )
        except ValidationError as e:
            return self._handle_error({e.code: e.message})

        try:
            member = Member.objects.get(email=email)
        except ObjectDoesNotExist:
            msg = f"ObjectDoesNotExist: Cannot find a Member with email '{email}'"
            return self._handle_error({"email": msg})

        member.is_active = True
        member.date_of_last_membership_payment = datetime.now(timezone.utc)
        member.membership_type = membership_type
        # Sync first and last name with whatever the User entered in the Zeffy form.
        member.first_name = first_name
        member.last_name = last_name

        try:
            # Run full_clean to validate membership_type choices.
            member.full_clean()
        except ValidationError as e:
            return self._handle_error({"error": {"message": e.messages}})

        member.save()

        return JsonResponse(
            {
                "email": email,
                "date_of_last_membership_payment": member.date_of_last_membership_payment,
                "is_active": True,
            },
            status=200,
        )
