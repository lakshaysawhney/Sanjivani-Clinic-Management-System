from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN"
        RECEPTIONIST = "RECEPTIONIST"
        THERAPIST = "THERAPIST"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.THERAPIST)
    full_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    pending_activation = models.BooleanField(default=True)


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="provider")
    display_name = models.CharField(max_length=60)
    specialization = models.CharField(max_length=60, blank=True)
    display_order = models.PositiveSmallIntegerField(default=100)

    class Meta:
        ordering = ["display_order", "id"]


class LoginAttempt(models.Model):
    key = models.CharField(max_length=64, unique=True)
    count = models.PositiveIntegerField(default=0)
    window = models.DateTimeField()


class CredentialToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    digest = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True)
