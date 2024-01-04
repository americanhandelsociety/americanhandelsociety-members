from random import choice

import pytest
from django.contrib.admin.sites import AdminSite

from americanhandelsociety_app.admin import (
    Admin,
    UpdatedPastMonthFilter,
    DuesPaymentStatusFilter,
    MessiahCircleFilter,
)
from americanhandelsociety_app.models import Member
from time_machine import travel

#############################
# last_updated FILTER TESTS #
#############################


@pytest.mark.django_db
def test_existing_members_dont_appear_in_filter_as_recently_updated(
    artificially_backdated_pre_004_migration_members,
):
    qs = Member.objects.all()
    updated_past_month_filter = UpdatedPastMonthFilter(
        None, {"updated_past_month": "updated"}, Member, Admin
    )
    filter_values = updated_past_month_filter.queryset(None, qs)
    assert filter_values.count() == 0


@pytest.mark.django_db
def test_existing_members_appear_in_filter_after_update(
    artificially_backdated_pre_004_migration_members, address
):
    qs = Member.objects.all()
    random_member = choice(qs)
    random_member.address = address
    random_member.save()
    updated_past_month_filter = UpdatedPastMonthFilter(
        None, {"updated_past_month": "updated"}, Member, Admin
    )
    filter_values = updated_past_month_filter.queryset(None, qs)
    assert filter_values.count() == 1
    assert random_member == filter_values[0]


@pytest.mark.django_db
def test_new_members_appear_in_filter_by_default(
    artificially_backdated_pre_004_migration_members, member
):
    qs = Member.objects.all()
    updated_past_month_filter = UpdatedPastMonthFilter(
        None, {"updated_past_month": "updated"}, Member, Admin
    )
    filter_values = updated_past_month_filter.queryset(None, qs)
    assert filter_values.count() == 1
    assert member == filter_values[0]


#####################################
# DUES PAYMENT STATUS FILTER  TESTS #
#####################################


@travel("2023-12-01")
@pytest.mark.django_db
def test_dues_payment_up_to_date_filter(mix_of_paid_and_overdue_members):
    admin_filter = DuesPaymentStatusFilter(
        None, {"dues_payment": "paid"}, Member, Admin
    )
    filter_values = admin_filter.queryset(None, Member.objects.all())
    assert filter_values.count() == 2
    assert all(
        member.date_of_last_membership_payment.year == 2023 for member in filter_values
    )


@travel("2023-12-01")
@pytest.mark.django_db
def test_dues_payment_outstanding_filter(mix_of_paid_and_overdue_members):
    admin_filter = DuesPaymentStatusFilter(
        None, {"dues_payment": "outstanding"}, Member, Admin
    )
    filter_values = admin_filter.queryset(None, Member.objects.all())
    assert filter_values.count() == 5
    assert all(
        member.date_of_last_membership_payment.year == 2022 for member in filter_values
    )


@travel("2023-12-01")
@pytest.mark.django_db
def test_dues_payment_no_keywords_on_filter(mix_of_paid_and_overdue_members):
    admin_filter = DuesPaymentStatusFilter(None, {}, Member, Admin)
    filter_values = admin_filter.queryset(None, Member.objects.all())
    assert filter_values.count() == 15


#####################################
# LIFETIME MEMBERSHIP FILTER TESTS #
#####################################


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
