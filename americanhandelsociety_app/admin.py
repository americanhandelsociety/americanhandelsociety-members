from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Member, Address


class Admin(UserAdmin):
    model = Member
    list_display = (
        "first_name",
        "last_name",
        "email",
        "id",
        "address",
        "updated_past_month",
    )

    def updated_past_month(self, obj):
        if not obj.last_updated:
            return None
        updated_past_month = obj.last_updated >= (
            datetime.utcnow().replace(tzinfo=timezone.utc) + relativedelta(days=-30)
        )
        return updated_past_month or None

    updated_past_month.short_description = "Updated Past Month?"

    list_filter = (
        "email",
        "available_in_directory",
        "address",
        "is_staff",
        "is_active",
        "id",
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
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Member, Admin)
admin.site.register(Address)
