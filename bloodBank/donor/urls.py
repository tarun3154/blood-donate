from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

app_name = 'donor'

urlpatterns = [
    path('donorlogin/', LoginView.as_view(template_name='donor/donorlogin.html'), name='donorlogin'),
    path('donorsignup/', views.donor_signup_view, name='donorsignup'),
]
