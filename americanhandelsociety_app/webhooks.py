import logging
from datetime import datetime, timezone

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from americanhandelsociety_app.models import Member

logger = logging.getLogger(__name__)


class MemberRenewalSerializer(serializers.ModelSerializer):
    confirmed_member_email = serializers.EmailField(required=False)

    class Meta:
        model = Member
        fields = [
            "email",
            "membership_type",
            "first_name",
            "last_name",
            "confirmed_member_email",
        ]
        # overwrite model constraints: (1) "membership_type" MUST BE included, and (2) do not apply email unique constraint
        extra_kwargs = {
            "membership_type": {"required": True, "allow_blank": False},
            "email": {"validators": []},
        }

    def to_internal_value(self, data):
        data_copy = data.copy()
        membership_type = data.get("membership_type")
        if membership_type:
            membership_type = Member.MembershipType.undo_friendly_name(membership_type)
            data_copy["membership_type"] = membership_type

        return super().to_internal_value(data_copy)


class MembershipRenewalWebhook(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = MemberRenewalSerializer

    def handle_error(self, error: dict, status_code: int = status.HTTP_400_BAD_REQUEST):
        logger.error(error)
        return Response(error, status=status_code)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get("confirmed_member_email") or serializer.data.get(
            "email"
        )

        try:
            member = Member.objects.get(email=email)
        except Member.DoesNotExist:
            msg = f"ObjectDoesNotExist: Cannot find a Member with email '{email}'"
            return self.handle_error({"error": {"message": msg}})

        member.is_active = True
        member.date_of_last_membership_payment = datetime.now(timezone.utc)
        member.membership_type = serializer.data.get("membership_type")
        member.first_name = serializer.data.get("first_name")
        member.last_name = serializer.data.get("last_name")

        try:
            member.full_clean()
        except ValidationError as e:
            return self.handle_error({"error": {"message": e.messages}})

        member.save()

        logger.info(f"Successful renewal! Member id starts with: {str(member.id)[0:8]}")

        return Response(
            {
                "member_email": email,
                "date_of_last_membership_payment": member.date_of_last_membership_payment,
                "is_active": True,
            },
            status=status.HTTP_200_OK,
        )
