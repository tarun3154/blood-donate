from django.shortcuts import render, HttpResponseRedirect
from .forms import DonorUserForm, DonorForm
from django.contrib.auth.models import Group

def donor_signup_view(request):
    userform = DonorUserForm()
    donorform = DonorForm()
    mydict = {'userform': userform, 'donorform': donorform}
    
    if request.method == "POST":
        userform = DonorUserForm(request.POST)
        donorform = DonorForm(request.POST, request.FILES)
        
        if userform.is_valid() and donorform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            
            donor = donorform.save(commit=False)
            donor.user = user
            donor.bloodgroup = donorform.cleaned_data['bloodgroup']
            donor.save()
            
            my_donor_group, created = Group.objects.get_or_create(name='DONOR')
            my_donor_group.user_set.add(user)
            
            return HttpResponseRedirect('donor/donorlogin')  # Use the correct URL

    return render(request, 'donor/donorsignup.html', context=mydict)
