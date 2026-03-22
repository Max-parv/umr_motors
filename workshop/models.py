from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Booking(models.Model):

    booking_code = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    name = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=10,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be exactly 10 digits."
            )
        ]
    )

    registration_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    VEHICLE_CHOICES = [
        ('Car', 'Car'),
        ('SUV', 'SUV'),
        ('Hatchback', 'Hatchback'),
        ('Sedan', 'Sedan'),
        ('Luxury', 'Luxury'),
    ]

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_CHOICES
    )

    problem_description = models.TextField()

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
        db_index=True
    )

    expected_completion_date = models.DateField(
        blank=True,
        null=True
    )

    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto generate booking code
        if not self.booking_code:
            year = timezone.now().year
            count = Booking.objects.count() + 1
            self.booking_code = f"UMR-{year}-{str(count).zfill(4)}"

        if self.registration_number:
            self.registration_number = self.registration_number.upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_code} - {self.name}"