from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Member, Address

from django.contrib.admin import SimpleListFilter


class UpdatedPastMonthFilter(SimpleListFilter):
    title = "Updated Past Month"
    parameter_name = "updated_past_month"

    def lookups(self, request, model_admin):
        return [
            ("updated", "Updated Past Month"),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        past_month = datetime.utcnow().replace(tzinfo=timezone.utc) - relativedelta(
            days=30
        )
        if self.value() == "updated":
            return queryset.filter(last_updated__gte=past_month)


class Admin(UserAdmin):
    model = Member
    list_display = (
        "first_name",
        "last_name",
        "email",
        "id",
        "address",
        "contact_preference",
        "date_of_last_membership_payment",
        "updated_past_month",
        "is_member_via_other_organization",
        "publish_member_name_consent",
    )

    def updated_past_month(self, obj):
        if not obj.last_updated:
            return None
        if obj.last_updated >= (
            datetime.utcnow().replace(tzinfo=timezone.utc) - relativedelta(days=30)
        ):
            return "Yes"
        return None

    updated_past_month.short_description = "Updated Past Month"

    list_filter = (
        "email",
        "available_in_directory",
        "publish_member_name_consent",
        "address",
        "contact_preference",
        "is_staff",
        "is_active",
        "id",
        UpdatedPastMonthFilter,
    )
    fieldsets = (
        ("Authentication", {"fields": ("email", "password")}),
        (
            "Member Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "address",
                    "membership_type",
                    "contact_preference",
                    "phone_number",
                    "institution",
                    "available_in_directory",
                    "date_of_last_membership_payment",
                    "is_member_via_other_organization",
                    "publish_member_name_consent",
                )
            },
        ),
        ("Authorization", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    ordering = (
        "email",
        "first_name",
        "last_name",
    )


admin.site.register(Member, Admin)
admin.site.register(Address)
