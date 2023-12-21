from random import choice

import pytest
from django.contrib.admin.sites import AdminSite

from americanhandelsociety_app.admin import (
    Admin,
    UpdatedPastMonthFilter,
    DuesPaymentStatus,
    MessiahCircleFilter,
)
from americanhandelsociety_app.models import Member
from time_machine import travel


##############################
# DUES PAYMENT STATUS FILTER #
##############################


@travel("2023-12-01")
@pytest.mark.django_db
def test_dues_payment_up_to_date_filter(mix_of_paid_and_overdue_members):
    admin_filter = DuesPaymentStatus(None, {"dues_payment": "paid"}, Member, Admin)
    filter_values = admin_filter.queryset(None, Member.objects.all())
    assert filter_values.count() == 2
    assert all(
        member.date_of_last_membership_payment.year == 2023 for member in filter_values
    )


@travel("2023-12-01")
@pytest.mark.django_db
def test_dues_payment_outstanding_filter(mix_of_paid_and_overdue_members):
    admin_filter = DuesPaymentStatus(
        None, {"dues_payment": "outstanding"}, Member, Admin
    )
    filter_values = admin_filter.queryset(None, Member.objects.all())
    assert filter_values.count() == 5
    assert all(
        member.date_of_last_membership_payment.year == 2022 for member in filter_values
    )


@travel("2023-12-01")
@pytest.mark.django_db
def test_dues_payment_not_applicable_filter(mix_of_paid_and_overdue_members):
    admin_filter = DuesPaymentStatus(
        None, {"dues_payment": "not_applicable"}, Member, Admin
    )
    filter_values = admin_filter.queryset(None, Member.objects.all())
    assert filter_values.count() == 4
    assert (
        filter_values.filter(
            membership_type=Member.MembershipType.MESSIAH_CIRCLE
        ).count()
        == 3
    ), "Messiah Circle members count unexpected"
    assert (
        filter_values.filter(is_member_via_other_organization=True).count() == 1
    ), "Other Org members count unexpeted"


@travel("2023-12-01")
@pytest.mark.django_db
def test_dues_payment_no_keywords_on_filter(mix_of_paid_and_overdue_members):
    admin_filter = DuesPaymentStatus(None, {}, Member, Admin)
    filter_values = admin_filter.queryset(None, Member.objects.all())
    assert filter_values.count() == 15


##############################
# LIFETIME MEMBERSHIP FILTER #
##############################


@pytest.mark.django_db
def test_lifetime_membership_filter(mix_of_paid_and_overdue_members):
    admin_filter = MessiahCircleFilter(
        None, {"lifetime_membership": "messiah_circle"}, Member, Admin
    )
    filter_values = admin_filter.queryset(None, Member.objects.all())
    assert filter_values.count() == 3
    assert all(
        member.membership_type == Member.MembershipType.MESSIAH_CIRCLE
        for member in filter_values
    )


@pytest.mark.django_db
def test_lifetime_membership_bad_params_filter(mix_of_paid_and_overdue_members):
    admin_filter = MessiahCircleFilter(
        None, {"lifetime_membership": "fitness"}, Member, Admin
    )
    filter_values = admin_filter.queryset(None, Member.objects.all())
    assert filter_values.count() == 15
