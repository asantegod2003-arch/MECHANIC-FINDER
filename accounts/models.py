from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("mechanic", "Mechanic"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    # ==========================
    # MECHANIC LIVE LOCATION
    # ==========================

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    # Whether the mechanic is available to receive jobs
    available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"