from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class RetailerManager(UserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class Retailer(AbstractUser):
    store_name = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    business_name = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(
        max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(default="")
    is_verified = models.BooleanField(default=False)

    objects = RetailerManager()

    # Add custom related_name attributes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='retailer_set',
        related_query_name='retailer',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='retailer_permission_set',
        related_query_name='retailer',
    )

    def __str__(self):
        return self.username
