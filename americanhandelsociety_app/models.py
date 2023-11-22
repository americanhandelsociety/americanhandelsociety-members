import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.forms.models import model_to_dict
from django.utils import timezone
from americanhandelsociety_app.utils import year_now


class MemberManager(BaseUserManager):
    """A custom manager for the Member model.

    This manager enables instantiating a new Member with the "email" as the "username."
    Reference: https://github.com/django/django/blob/2a76f4313423a3b91caade4fce71790630ef9152/tests/auth_tests/models/custom_user.py#L8-L33
    """

    def create_user(self, email, password=None, **fields):
        """Creates and saves a user (Member) with the given email and
        password."""
        if not email:
            raise ValueError("Members/users must have an email address")

        user = self.model(email=self.normalize_email(email), **fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **fields):
        superuser = self.create_user(email, password=password, **fields)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser

    def dues_payment_pending(self):
        """Select members with overdue payments.

        Excludes:
        - lifetime membership members (Messiah Circle)
        - members with membership via partner organizations
        - members with payments in the current calendar year
        - previous members, who haven't paid in > calendar year
        """
        return self.exclude(
            models.Q(is_member_via_other_organization=True)
            | models.Q(membership_type=self.model.MembershipType.MESSIAH_CIRCLE)
        ).filter(date_of_last_membership_payment__year=year_now() - 1)


class Member(AbstractUser):
    class MembershipType(models.TextChoices):
        REGULAR = "REGULAR", "40.00"
        STUDENT = "STUDENT", "20.00"
        RETIRED = "RETIRED", "20.00"
        JOINT = "JOINT", "50.00"
        RINALDO_CIRCLE = "RINALDO_CIRCLE", "75.00"
        CLEOPATRA_CIRCLE = "CLEOPATRA_CIRCLE", "125.00"
        THEODORA_CIRCLE = "THEODORA_CIRCLE", "250.00"
        MESSIAH_CIRCLE = "MESSIAH_CIRCLE", "500.00"

        @classmethod
        def max_length(cls):
            return max(*(len(choice.value) for choice in cls))

    class ContactPreference(models.TextChoices):
        PRINT = "PRINT"
        EMAIL = "EMAIL"
        BOTH = "BOTH"

        @classmethod
        def max_length(cls):
            return max(*(len(choice.value) for choice in cls))

    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    username = None
    first_name = models.CharField(max_length=150, verbose_name="first name")
    last_name = models.CharField(max_length=150, verbose_name="last name")
    email = models.EmailField(
        error_messages={"unique": "A member with that email already exists."},
        max_length=150,
        unique=True,
        verbose_name="email",
    )
    membership_type = models.CharField(
        max_length=MembershipType.max_length(),
        choices=MembershipType.choices,
        blank=True,
    )
    available_in_directory = models.BooleanField(default=False)
    contact_preference = models.CharField(
        max_length=ContactPreference.max_length(),
        choices=ContactPreference.choices,
        blank=False,
    )
    phone_number = models.CharField(max_length=15, blank=True)
    institution = models.CharField(max_length=150, blank=True)
    address = models.ForeignKey(
        "Address", on_delete=models.CASCADE, null=True, blank=True
    )
    is_member_via_other_organization = models.BooleanField(
        default=False,
        help_text="Denotes if the member pays dues through a 'sister' organization, such as the Georg-Friedrich-Händel-Gesellschaft.",
    )
    date_of_last_membership_payment = models.DateTimeField(default=timezone.now)
    accepts_privacy_policy = models.BooleanField(default=False)
    last_updated = models.DateTimeField(
        auto_now=True,
        null=True,
    )
    objects = MemberManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


class Address(models.Model):
    street_address = models.CharField(max_length=500)
    street_address_2 = models.CharField(max_length=500, blank=True)
    street_address_3 = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state_province_region = models.CharField(max_length=150, blank=True)
    zip_postal_code = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        full_address_values = [
            val for val in model_to_dict(self, exclude=["id"]).values() if val
        ]

        return f"{', '.join(full_address_values)}"
