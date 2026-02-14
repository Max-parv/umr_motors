from workshop.views import home, booking, dashboard, manage_bookings, customer_login
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('booking/', booking, name='booking'),
    path('dashboard/', dashboard, name='dashboard'),
    path('manage-bookings/', manage_bookings, name='manage_bookings'),
    path('track/', customer_login, name='customer_login'),  # NEW
]
