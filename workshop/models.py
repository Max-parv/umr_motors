import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone


# -----------------------------
# Booking Model
# -----------------------------
class Booking(models.Model):
    booking_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, db_index=True)
    vehicle_type = models.CharField(max_length=50)
    problem_description = models.TextField()

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booking_date']
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.booking_id} - {self.name}"


# -----------------------------
# OTP Verification Model
# -----------------------------
class OTPVerification(models.Model):
    phone = models.CharField(max_length=15, db_index=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.phone} - {self.otp}"
