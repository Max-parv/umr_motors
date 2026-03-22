from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "booking_code",
        "name",
        "phone",
        "registration_number",
        "vehicle_type",
        "status",
        "final_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "vehicle_type",
        "created_at",
    )

    search_fields = (
        "booking_code",
        "name",
        "phone",
        "registration_number",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "booking_code",
        "created_at",
        "updated_at",
    )