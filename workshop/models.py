import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


# =====================================================
# Booking Model
# =====================================================
class Booking(models.Model):

    booking_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    name = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=10,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be 10 digits."
            )
        ]
    )

    registration_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

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

    # ✅ Expected Completion Date
    expected_completion_date = models.DateField(
        null=True,
        blank=True
    )

    # ✅ Final Service Amount (Revenue Tracking)
    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-booking_date']
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        if self.registration_number:
            self.registration_number = self.registration_number.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.name}"


# =====================================================
# OTP Verification Model
# =====================================================
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
