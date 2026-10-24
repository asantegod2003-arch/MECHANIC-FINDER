from django.db import models
from django.contrib.auth.models import User


class RescueRequest(models.Model):

    STATUS_CHOICES = (

        ("pending", "Pending"),

        ("accepted", "Accepted"),

        ("on_the_way", "On The Way"),

        ("arrived", "Arrived"),

        ("completed", "Completed"),

        ("cancelled", "Cancelled"),

    )


    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rescue_requests"
    )


    mechanic = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_jobs"
    )


    vehicle_problem = models.CharField(
        max_length=200
    )


   
    location = models.CharField(
    max_length=255,
    help_text="Town, landmark or street"
)


    phone_number = models.CharField(
        max_length=20
    )


    # ==========================
    # GPS LOCATION
    # ==========================

    customer_latitude = models.FloatField(
        null=True,
        blank=True
    )

    customer_longitude = models.FloatField(
        null=True,
        blank=True
    )

    mechanic_latitude = models.FloatField(
        null=True,
        blank=True
    )

    mechanic_longitude = models.FloatField(
        null=True,
        blank=True
    )


    # ==========================
    # STATUS
    # ==========================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f"{self.customer.username} - {self.status}"