from django.contrib.auth.models import AbstractUser
from django.db import models


class Passenger(AbstractUser):
    country_code = models.CharField(
        max_length=5, blank=False, null=False)
    contact_number = models.CharField(
        max_length=15, blank=False, null=False)
