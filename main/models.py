# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('DONOR', 'Donor'),
        ('PATIENT', 'Patient'),
        ('AUTHORITY', 'Authority'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class BloodInventory(models.Model):
    BLOOD_TYPE_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    units_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.blood_type} - {self.units_available} units"

class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BloodInventory.BLOOD_TYPE_CHOICES)
    blood_units = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_type}"

class PatientRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BloodInventory.BLOOD_TYPE_CHOICES)
    units_required = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_type} request"
