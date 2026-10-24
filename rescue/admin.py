from django.contrib import admin
from .models import RescueRequest


@admin.register(RescueRequest)
class RescueRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "mechanic",
        "vehicle_problem",
        "location",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "customer__username",
        "mechanic__username",
        "location",
        "vehicle_problem",
        "phone_number",
    )
