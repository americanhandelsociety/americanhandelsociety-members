from django.contrib import admin
from django.urls import path, include

from americanhandelsociety_app.views import (
    Join,
    Pay,
    PaymentConfirmation,
    Profile,
    Login,
    Logout,
    Home,
    Events,
    ResearchMaterials,
    Donate,
    People,
    Profile,
    Login,
    Logout,
    PasswordChange,
    EditMember,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("events/", Events.as_view(), name="events"),
    path("research-materials/", ResearchMaterials.as_view(), name="research-materials"),
    path("donate/", Donate.as_view(), name="donate"),
    path("people/", People.as_view(), name="people"),
    # Profile
    path("profile/", Profile.as_view(), name="profile"),
    path("change-password/", PasswordChange.as_view(), name="change-password"),
    path("edit-member/<str:member_uuid>", EditMember.as_view(), name="edit-member"),
    # Auth
    path("logout/", Logout.as_view(), name="logout"),
    path("login/", Login.as_view(), name="login"),
    path("admin/", admin.site.urls),
    # Paypal
    path("join/", Join.as_view(), name="join"),
    path("pay/", Pay.as_view(), name="pay"),
    path("pay-confirm/", PaymentConfirmation.as_view(), name="pay-confirm"),
    path("paypal/", include("paypal.standard.ipn.urls")),
    # Django captcha
    path("captcha/", include("captcha.urls")),
]
