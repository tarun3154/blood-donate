from django import forms

from .models import *


class BloodForm(forms.ModelForm):
    class Meta:
        model=Stock
        fields=['bloodgroup','unit']

class RequestForm(forms.ModelForm):
    class Meta:
        model=BloodRequest
        fields=['patient_name','patient_age','reason','bloodgroup','unit']





class DonationConfirmationForm(forms.Form):
    donated_unit = forms.IntegerField(
        label='Units Donated',
        min_value=1,  # You can set the minimum value as per your requirements
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    donor_name = forms.CharField(
        label='Donor Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )