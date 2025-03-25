from django.contrib.auth.models import AbstractUser
from django.db import models


class Retailer(AbstractUser):
    store_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username
