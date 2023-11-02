from django.shortcuts import render, HttpResponseRedirect,redirect
from .forms import *
from .models import *
from blood.models import *

from django.contrib.auth.models import Group

def donor_signup_view(request):
    userForm=DonorUserForm()
    donorForm=DonorForm()
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=DonorUserForm(request.POST)
        donorForm=DonorForm(request.POST,request.FILES)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            my_donor_group = Group.objects.get_or_create(name='DONOR')
            my_donor_group[0].user_set.add(user)
        return redirect('donor:donorlogin')
    return render(request,'donor/donorsignup.html',context=mydict)

def donor_dashboard_view(request):
    donor= Donor.objects.get(user_id=request.user.id)
    dict={
        'requestpending': BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Pending').count(),
        'requestapproved': BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Approved').count(),
        'requestmade': BloodRequest.objects.all().filter(request_by_donor=donor).count(),
        'requestrejected': BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Rejected').count(),
    }
    return render(request,'donor/donor_dashboard.html',context=dict)

def donate_blood_view(request):
    donation_form= DonationForm()
    if request.method == 'POST':
        donation_form= DonationForm(request.POST)
        if donation_form.is_valid():
            blood_donate= donation_form.save(commit=False)
            blood_donate.group =donation_form.cleaned_data['bloodgroup']
            donor= Donor.objects.get(user_id = request.user.id)
            blood_donate.donor= donor
            blood_donate.save()
        return redirect('donor:donation-history')  
    return render(request,'donor/donate_blood.html',{'donation_form':donation_form})
        

def donation_history_view(request):
    donor=Donor.objects.get(user_id=request.user.id)
    donations= BloodDonate.objects.all().filter(donor=donor)
    return render(request,'donor/donation_history.html',{'donations':donations})
    
            