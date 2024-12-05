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


class ProtectedAPIView(LoginRequiredMixin):
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "403 Forbidden"}, status=403)

        return super().dispatch(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class MembershipRenewalWebhook(ProtectedAPIView, View):
    def _handle_error(self, error: dict, status_code: int = 400):
        logger.error(error)
        return JsonResponse(error, status=status_code)

    def _validate_required_field(self, field_name, value):
        if not value:
            raise ValidationError("Required field.", code=field_name)

        return value

    def post(self, request):
        try:
            member_uuid = self._validate_required_field(
                field_name="member_uuid", value=request.POST.get("member_uuid")
            )
            membership_type = self._validate_required_field(
                field_name="membership_type", value=request.POST.get("membership_type")
            )
        except ValidationError as e:
            return self._handle_error({e.code: e.message})

        try:
            member = Member.objects.get(id=member_uuid)
        except ValidationError as e:
            return self._handle_error({"member_uuid": "Not a valid UUID."})
        except ObjectDoesNotExist:
            msg = f"ObjectDoesNotExist: Cannot find a Member with id '{member_uuid}'"
            return self._handle_error({"member_uuid": msg})

        member.is_active = True
        member.membership_type = membership_type
        member.date_of_last_membership_payment = datetime.now(timezone.utc)

        try:
            # Run full_clean to validate membership_type choices.
            member.full_clean()
        except ValidationError as e:
            return self._handle_error({"error": {"message": e.messages}})

        member.save()

        return JsonResponse(
            {
                "member_uuid": member_uuid,
                "date_of_last_membership_payment": member.date_of_last_membership_payment,
                "is_active": True,
            },
            status=200,
        )
