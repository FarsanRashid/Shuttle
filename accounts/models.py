from datetime import timedelta
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Passenger(AbstractUser):
    country_code = models.CharField(
        max_length=5, blank=False, null=False)
    contact_number = models.CharField(
        max_length=15, blank=False, null=False)


class TokenStore(models.Model):
    key = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='tokens', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.key.hex

    def is_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Token expires in 1 hour by default
            self.expires_at = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)
