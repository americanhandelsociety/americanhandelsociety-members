from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class MemberManager(BaseUserManager):
    """
    A custom manager for the Member model.

    This manager enables instantiating a new Member with the "email" as the "username."
    Reference: https://github.com/django/django/blob/2a76f4313423a3b91caade4fce71790630ef9152/tests/auth_tests/models/custom_user.py#L8-L33
    """

    def create_user(self, email, password=None, **fields):
        """
        Creates and saves a user (Member) with the given email and password.
        """
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
    username = None
    first_name = models.CharField(max_length=150, verbose_name="first name")
    last_name = models.CharField(max_length=150, verbose_name="last name")
    email = models.EmailField(
        error_messages={"unique": "A member with that email already exists."},
        max_length=150,
        unique=True,
        verbose_name="email",
    )
    available_in_directory = models.BooleanField(default=True)
    address = models.ForeignKey(
        "Address", on_delete=models.CASCADE, null=True, blank=True
    )

    objects = MemberManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


class Address(models.Model):
    street_address = models.CharField(max_length=500)
    street_address_2 = models.CharField(max_length=500)
    city = models.CharField(max_length=150)
    state_province_region = models.CharField(max_length=150)
    zip_postal_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.street_address
