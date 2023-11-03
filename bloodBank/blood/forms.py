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
