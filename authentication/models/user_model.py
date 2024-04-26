from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str = None,
        **extra_fields
    ) -> "User":
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if not email:
            raise ValueError("Email is required.")
        if not first_name:
            raise ValueError("first name is required.")
        if not last_name:
            raise ValueError("last name is required.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(
        self, first_name: str, last_name: str, email: str, password: str
    ) -> "User":
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.save()
        return user


class User(AbstractUser):

    first_name = models.CharField(
        verbose_name="First Name",
        max_length=255,
    )
    last_name = models.CharField(
        verbose_name="Last Name",
        max_length=255,
    )
    email = models.EmailField(verbose_name="email", max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = "test_auth_user"
        ordering = ["first_name"]
