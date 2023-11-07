# blood/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from blood.models import BloodRequest, DonationRequest
from donor.models import Donor

@receiver(post_save, sender=BloodRequest)
def create_donation_request(sender, instance, created, **kwargs):
    if created and instance.unit == 0:
        eligible_donors = Donor.objects.filter(bloodgroup=instance.bloodgroup)
        for donor in eligible_donors:
            donated_units = 1  
            DonationRequest.objects.create(
                bloodgroup=instance.bloodgroup,
                donor_name=donor.donor_name,
                units_donated=donated_units,
            )

@receiver(post_save, sender=DonationRequest)
def notify_donors(sender, instance, created, **kwargs):
    if created:
        eligible_donors = Donor.objects.filter(bloodgroup=instance.bloodgroup)
        for donor in eligible_donors:
            message = f'There is a new blood donation request for {instance.bloodgroup}. Please consider donating.'
            messages.info(donor.user, message)
