from django.contrib import admin
from django.urls import path
from workshop import views

urlpatterns = [

    # Django Admin
    path("admin/", admin.site.urls),

    # Public
    path("", views.home, name="home"),
    path("booking/", views.booking, name="booking"),
    path("track/", views.customer_login, name="customer_login"),

    # Workshop Auth
    path("workshop-login/", views.workshop_login, name="workshop_login"),
    path("workshop-logout/", views.workshop_logout, name="workshop_logout"),

    # Staff Panel
    path("dashboard/", views.dashboard, name="dashboard"),
    path("manage-bookings/", views.manage_bookings, name="manage_bookings"),
]