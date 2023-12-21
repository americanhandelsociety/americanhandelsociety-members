from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q

from .models import Member, Address

from django.contrib.admin import SimpleListFilter
from americanhandelsociety_app.utils import year_now


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


class DuesPaymentStatus(SimpleListFilter):
    title = "Dues Payment"
    parameter_name = "dues_payment"

    def lookups(self, request, model_admin):
        return [
            ("paid", "Dues Paid Current Year"),
            ("outstanding", "Dues Outstanding Current Year"),
            ("not_applicable", "Dues Payment Not-Applicable"),
        ]

    def queryset(self, request, queryset):
        return {
            "paid": queryset.exclude(
                Q(is_member_via_other_organization=True)
                | Q(membership_type=queryset.model.MembershipType.MESSIAH_CIRCLE)
            ).filter(date_of_last_membership_payment__year=year_now()),
            "outstanding": queryset.exclude(
                Q(is_member_via_other_organization=True)
                | Q(membership_type=queryset.model.MembershipType.MESSIAH_CIRCLE)
            ).filter(date_of_last_membership_payment__year=year_now() - 1),
            "not_applicable": queryset.filter(
                Q(is_member_via_other_organization=True)
                | Q(membership_type=queryset.model.MembershipType.MESSIAH_CIRCLE)
            ),
        }.get(self.value(), queryset)


class MessiahCircleFilter(SimpleListFilter):
    title = "Messiah Circle Members"
    parameter_name = "lifetime_membership"

    def lookups(self, request, model_admin):
        return [("messiah_circle", "Messiah Circle Lifetime Members")]

    def queryset(self, request, queryset):
        val = self.value()
        if not val or val != "messiah_circle":
            return queryset
        return queryset.filter(
            membership_type=queryset.model.MembershipType.MESSIAH_CIRCLE
        )


class Admin(UserAdmin):
    model = Member
    list_display = (
        "first_name",
        "last_name",
        "membership",
        "email",
        "id",
        "address",
        "contact_preference",
        "date_of_last_membership_payment",
        "updated_past_month",
        "is_member_via_other_organization",
        "dues_paid_current_calendar_year",
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
        "address",
        "contact_preference",
        "is_staff",
        "is_active",
        "id",
        UpdatedPastMonthFilter,
        DuesPaymentStatus,
        MessiahCircleFilter,
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
