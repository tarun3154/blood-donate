from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Sum,Q

from donor.models import *
from patient.models import *
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *

from donor.forms import *
from patient.forms import *

def home_view(request):
    x=Stock.objects.all()
    if len(x)==0:
        blood1=models.Stock()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=models.Stock()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=models.Stock()
        blood3.bloodgroup="B+"
        blood3.save()        

        blood4=models.Stock()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=models.Stock()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=models.Stock()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=models.Stock()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=models.Stock()
        blood8.bloodgroup="O-"
        blood8.save()

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'blood/index.html')

def is_donor(user):
    return user.groups.filter(name='DONOR').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


def afterlogin_view(request):
    if is_donor(request.user):      
        return redirect('donor:donor-dashboard')
                
    elif is_patient(request.user):
        return redirect('patient:patient-dashboard')
    else:
        return redirect('admin-dashboard')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    totalunit=Stock.objects.aggregate(Sum('unit'))
    dict={

        'A1':Stock.objects.get(bloodgroup="A+"),
        'A2':Stock.objects.get(bloodgroup="A-"),
        'B1':Stock.objects.get(bloodgroup="B+"),
        'B2':Stock.objects.get(bloodgroup="B-"),
        'AB1':Stock.objects.get(bloodgroup="AB+"),
        'AB2':Stock.objects.get(bloodgroup="AB-"),
        'O1':Stock.objects.get(bloodgroup="O+"),
        'O2':Stock.objects.get(bloodgroup="O-"),
        'totaldonors':Donor.objects.all().count(),
        'totalbloodunit':totalunit['unit__sum'],
        'totalrequest':BloodRequest.objects.all().count(),
        'totalapprovedrequest':BloodRequest.objects.all().filter(status='Approved').count()
    }
    return render(request,'blood/admin_dashboard.html',context=dict)


@login_required(login_url='adminlogin')
def admin_blood_view(request):
    dict={
        'bloodForm':BloodForm(),
        'A1':Stock.objects.get(bloodgroup="A+"),
        'A2':Stock.objects.get(bloodgroup="A-"),
        'B1':Stock.objects.get(bloodgroup="B+"),
        'B2':Stock.objects.get(bloodgroup="B-"),
        'AB1':Stock.objects.get(bloodgroup="AB+"),
        'AB2':Stock.objects.get(bloodgroup="AB-"),
        'O1':Stock.objects.get(bloodgroup="O+"),
        'O2':Stock.objects.get(bloodgroup="O-"),
    }
    if request.method=='POST':
        bloodForm=forms.BloodForm(request.POST)
        if bloodForm.is_valid() :        
            bloodgroup=bloodForm.cleaned_data['bloodgroup']
            stock=models.Stock.objects.get(bloodgroup=bloodgroup)
            stock.unit=bloodForm.cleaned_data['unit']
            stock.save()
        return redirect('admin-blood')
    return render(request,'blood/admin_blood.html',context=dict)


@login_required(login_url='adminlogin')
def admin_donor_view(request):
    donors=dmodels.Donor.objects.all()
    return render(request,'blood/admin_donor.html',{'donors':donors})



@login_required(login_url='adminlogin')
def update_donor_view(request,pk):
    donor= Donor.objects.get(id=pk)
    user= User.objects.get(id=donor.user_id)
    userForm = DonorUserForm(instance= user)
    donorForm= DonorForm(request.FILES,instance=user)
    mydict={'userForm':userForm,'donorForm':donorForm}

    if request.method == 'POST':
        userForm=DonorUserForm(request.POST,instance=user)
        donorForm=DonorForm(request.POST,request.FILES,instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor = donorForm.save(commit=False)
            donor.user= user
            donor.bloodgroup= donorForm.cleaned_data['bloodgroup']
            donor.save()
            return redirect('admin-donor')
    return render(request,'blood/update_donor.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_donor_view(request,pk):
    donor= Donor.objects.get(id=pk)
    user = User.objects.get(id=donor.user_id)
    user.delete()
    donor.delete()
    return redirect('admin-donor')

@login_required(login_url='adminlogin')
def admin_patient_view(request):
    patients=pmodels.Patient.objects.all()
    return render(request,'blood/admin_patient.html',{'patients':patients})


@login_required(login_url='adminlogin')
def update_patient_view(request,pk):
    patient=pmodels.Patient.objects.get(id=pk)
    user=pmodels.User.objects.get(id=patient.user_id)
    userForm=PatientUserForm(instance=user)
    patientForm=PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=PatientUserForm(request.POST,instance=user)
        patientForm=PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            return redirect('admin-patient')
    return render(request,'blood/update_patient.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_patient_view(request,pk):
    patient = Patient.objects.get(id=pk)
    user= User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return HttpResponseRedirect('/admin-patient')


@login_required(login_url='adminlogin')
def admin_request_view(request):
    requests= BloodRequest.objects.all().filter(status = 'Pending')
    return render(request,'blood/admin_request.html',{'requests':requests})


@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    requests = BloodRequest.objects.all().exclude(status = 'Pending')
    return render(request,'blood/admin_request_history.html',{'requests':requests})

@login_required(login_url='adminlogin')
def admin_donation_view(request):
    donations=dmodels.BloodDonate.objects.all()
    return render(request,'blood/admin_donation.html',{'donations':donations})


@login_required(login_url='adminlogin')
def update_approve_status_view(request,pk):
    req=BloodRequest.objects.get(id=pk)
    message=None
    bloodgroup=req.bloodgroup
    unit=req.unit
    stock=Stock.objects.get(bloodgroup=bloodgroup)
    if stock.unit > unit:
        stock.unit=stock.unit-unit
        stock.save()
        req.status="Approved"
        
    else:
        message="Stock Doest Not Have Enough Blood To Approve This Request, Only "+str(stock.unit)+" Unit Available"
    req.save()

    requests=BloodRequest.objects.all().filter(status='Pending')
    return render(request,'blood/admin_request.html',{'requests':requests,'message':message})


@login_required(login_url='adminlogin')
def update_reject_status_view(request,pk):
    req=models.BloodRequest.objects.get(id=pk)
    req.status="Rejected"
    req.save()
    return redirect('/admin-request')





@login_required(login_url='adminlogin')
def approve_donation_view(request,pk):
    donation = BloodDonate.objects.get(id=pk)
    donation_blood_group= donation.bloodgroup
    donation_blood_unit = donation.unit

    stock = Stock.objects.get(bloodgroup=donation_blood_group)
    stock.unit=stock.unit+donation_blood_unit
    stock.save()

    donation.status = 'Approved'
    donation.save()
    return redirect('admin-donation')


@login_required(login_url='adminlogin')
def reject_donation_view(request,pk):
    donation=BloodDonate.objects.get(id=pk)
    donation.status='Rejected'
    donation.save()
    return redirect('admin-donation')