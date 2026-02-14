from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'vehicle_type', 'status', 'booking_date')
    list_filter = ('status',)
    search_fields = ('name', 'phone', 'vehicle_type')
