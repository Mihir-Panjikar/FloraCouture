from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class RetailerManager(UserManager):
    """
    Custom manager for the Retailer model.
    """

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
    business_name = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    is_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="retailers", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="retailers_permissions", blank=True)

    objects = RetailerManager()  # Assigning the custom manager

    def __str__(self):
        return self.business_name
