from django.contrib import admin
from django.urls import path
from workshop import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),

    path('track/', views.customer_login, name='customer_login'),
]
