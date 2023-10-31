from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Sum,Q

from donor import models as dmodels
from patient import models as pmodels
from donor import forms as dforms
from patient import forms as pforms
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *

def home_view(request):
    x=models.Stock.objects.all()
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
        'totaldonors':dmodels.Donor.objects.all().count(),
        'totalbloodunit':totalunit['unit__sum'],
        'totalrequest':models.BloodRequest.objects.all().count(),
        'totalapprovedrequest':models.BloodRequest.objects.all().filter(status='Approved').count()
    }
    return render(request,'blood/admin_dashboard.html',context=dict)
