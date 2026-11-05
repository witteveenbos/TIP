from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):  # type: ignore[django-manager-missing]
    organization = models.CharField(max_length=255, blank=True)
