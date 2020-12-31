from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Member, Address


class Admin(UserAdmin):
    model = Member
    list_display = (
        "first_name",
        "last_name",
        "email",
    )
    list_filter = (
        "email",
        "available_in_directory",
        "address",
        "is_staff",
        "is_active",
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
                    "available_in_directory",
                )
            },
        ),
        ("Authorization", {"fields": ("is_staff", "is_active")}),
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