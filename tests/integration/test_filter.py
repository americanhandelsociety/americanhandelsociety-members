from random import choice

import pytest
from django.contrib.admin.sites import AdminSite

from americanhandelsociety_app.admin import Admin, UpdatedPastMonthFilter
from americanhandelsociety_app.models import Member


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


@pytest.mark.django_db
def test_filter_matches_admin_updated_past_month(
    artificially_backdated_pre_004_migration_members, member, address
):
    qs = Member.objects.all()
    random_member = choice(artificially_backdated_pre_004_migration_members)
    random_member.address = address
    random_member.save()
    admin = Admin(Member, AdminSite)
    expected_in_qs_filter = [x for x in qs if admin.updated_past_month(x)]
    assert len(expected_in_qs_filter) == 2
    updated_past_month_filter = UpdatedPastMonthFilter(
        None, {"updated_past_month": "updated"}, Member, Admin
    )
    filter_values = updated_past_month_filter.queryset(None, qs)
    assert filter_values.count() == 2
    for m in expected_in_qs_filter:
        assert m in filter_values
