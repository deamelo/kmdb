from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    birthdate = models.DateField()
    bio = models.TextField(null=True, blank=True, default=None)
    is_critic = models.BooleanField(null=True, blank=True, default=False)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["first_name", "last_name", "email", "birthdate"]
