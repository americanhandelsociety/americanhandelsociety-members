import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


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


class Member(AbstractUser):
    class MembershipType(models.TextChoices):
        REGULAR = "REGULAR", "35.00"
        JOINT = "JOINT", "42.00"
        DONOR = "DONOR", "56.00"
        STUDENT = "STUDENT", "20.00"
        RETIRED = "RETIRED", "20.00"
        SPONSOR = "SPONSOR", "100.00"
        PATRON = "PATRON", "200.00"
        LIFE = "LIFE", "500.00"
        SUBSCRIBER = "SUBSCRIBER", "42.00"

        @classmethod
        def max_length(cls):
            return max(*(len(choice.value) for choice in cls))

    class ContactPreference(models.TextChoices):
        PRINT = "PRINT"
        EMAIL = "EMAIL"
        ALL = "ALL"

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
        blank=True,
    )
    phone_number = models.CharField(max_length=15, blank=True)
    institution = models.CharField(max_length=150, blank=True)
    address = models.ForeignKey(
        "Address", on_delete=models.CASCADE, null=True, blank=True
    )
    date_of_last_membership_payment = models.DateTimeField(auto_now_add=True)

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
        return self.street_address
