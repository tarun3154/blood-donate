from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from blood.models import DonationRequest
from donor.models import Donor

@receiver(post_save, sender=DonationRequest)
def notify_donors(sender, instance, created, **kwargs):
    if created:
        eligible_donors = Donor.objects.filter(bloodgroup=instance.blood_group)
        for donor in eligible_donors:
            message = f'There is a new blood donation request for {instance.blood_group}. Please consider donating.'
            messages.info(donor.user, message)
