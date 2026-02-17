from django.contrib import admin
from .models import Booking, OTPVerification


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'name', 'phone', 'vehicle_type', 'status', 'booking_date')
    list_filter = ('status',)
    search_fields = ('name', 'phone', 'vehicle_type')
    ordering = ('-booking_date',)


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'otp', 'is_verified', 'attempts', 'created_at')
    search_fields = ('phone',)
    ordering = ('-created_at',)
