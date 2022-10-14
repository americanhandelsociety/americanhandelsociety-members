from django.contrib import admin
from django.urls import path, include

from americanhandelsociety_app.views import (
    Join,
    Pay,
    PaymentConfirmation,
    PrivacyPolicy,
    Profile,
    Login,
    Logout,
    Home,
    Events,
    Awards,
    Newsletter,
    Renew,
    ResearchMaterials,
    Donate,
    People,
    Profile,
    Login,
    Logout,
    PasswordChange,
    EditMember,
    JoinOtherOrganizations,
)
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("events/", Events.as_view(), name="events"),
    path("awards/", Awards.as_view(), name="awards"),
    path("newsletter/", Newsletter.as_view(), name="newsletter"),
    path("research-materials/", ResearchMaterials.as_view(), name="research-materials"),
    path("donate/", Donate.as_view(), name="donate"),
    path("people/", People.as_view(), name="people"),
    path("privacy-policy", PrivacyPolicy.as_view(), name="privacy-policy"),
    # Profile
    path("profile/", Profile.as_view(), name="profile"),
    path("change-password/", PasswordChange.as_view(), name="change-password"),
    path("edit-member/<str:member_uuid>", EditMember.as_view(), name="edit-member"),
    path(
        "join-other-organizations/",
        JoinOtherOrganizations.as_view(),
        name="join-other-organizations",
    ),
    # Auth
    path("logout/", Logout.as_view(), name="logout"),
    path("login/", Login.as_view(), name="login"),
    path("admin/", admin.site.urls),
    path("reset/", PasswordResetView.as_view(), name="reset_password"),
    path("reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "reset/<uidb64>/<token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Paypal
    path("join/", Join.as_view(), name="join"),
    path("pay/", Pay.as_view(), name="pay"),
    path("pay-confirm/", PaymentConfirmation.as_view(), name="pay-confirm"),
    path("renew/", Renew.as_view(), name="renew"),
    path("paypal/", include("paypal.standard.ipn.urls")),
    # Django captcha
    path("captcha/", include("captcha.urls")),
]

# Errors
handler404 = "americanhandelsociety_app.views.page_not_found"
