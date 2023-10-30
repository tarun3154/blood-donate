from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponseRedirect
from .forms import PatientUserForm, PatientForm
from .models import Patient
from donor.models import Donor

def patient_signup_view(request):
    userForm = PatientUserForm()
    patientForm = PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    
    if request.method == 'POST':
        userForm = PatientUserForm(request.POST)
        patientForm = PatientForm(request.POST, request.FILES)
        
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.bloodgroup = patientForm.cleaned_data['bloodgroup']
            patient.save()

            my_patient_group, created = Group.objects.get_or_create(name='PATIENT')
            my_patient_group.user_set.add(user)
            
            return HttpResponseRedirect('patient/patientlogin')

    return render(request, 'patient/patientsignup.html', context=mydict)
