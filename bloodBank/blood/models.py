from .models import *
from donor.models import *
from patient.models import *

from enum import Enum
from .enums import BloodGroup
from django.db.models.signals import post_save
from django.dispatch import receiver






class Stock(models.Model):
    bloodgroup = models.CharField(max_length=5, choices=[(blood.value, blood.name) for blood in BloodGroup])
    unit = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.bloodgroup

class BloodRequest(models.Model):
    request_by_patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    request_by_donor = models.ForeignKey(Donor, null=True, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=30)
    patient_age = models.PositiveIntegerField()
    reason = models.CharField(max_length=500)
    bloodgroup = models.CharField(max_length=5, choices=[(blood.value, blood.name) for blood in BloodGroup])
    unit = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="Pending")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.bloodgroup

class DonationRequest(models.Model):
    bloodgroup = models.CharField(max_length=5, choices=[(blood.value, blood.name) for blood in BloodGroup])
    donor_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    units_donated = models.PositiveIntegerField(default=0)
    is_fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"Request for {self.bloodgroup} by {self.donor_name}"
