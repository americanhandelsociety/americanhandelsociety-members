from django.contrib import admin
from django.urls import path, re_path, include

from americanhandelsociety_app.views import (
    Join,
    Profile,
    Login,
    Logout,
    About,
    People,
    Profile,
    Login,
    Logout,
    PasswordChange,
    EditMember,
)

urlpatterns = [
    path("about/", About.as_view(), name="about"),
    path("people/", People.as_view(), name="people"),
    # Profile
    path("profile/", Profile.as_view(), name="profile"),
    re_path(r"^profile/(?P<form_name>.+)$", Profile.as_view(), name="success"),
    path("change-password/", PasswordChange.as_view(), name="change-password"),
    path("edit-member/<str:member_uuid>", EditMember.as_view(), name="edit-member"),
    # Auth
    path("logout/", Logout.as_view(), name="logout"),
    path("login/", Login.as_view(), name="login"),
    path("admin/", admin.site.urls),
    # Paypal
    path("join/", Join.as_view(), name="join"),
    path("paypal/", include("paypal.standard.ipn.urls")),
]
