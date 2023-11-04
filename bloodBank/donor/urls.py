from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

app_name = 'donor'

urlpatterns = [
    path('donorsignup/', views.donor_signup_view, name='donorsignup'),
    path('donorlogin/', LoginView.as_view(template_name='donor/donorlogin.html'), name='donorlogin'),
    path('donor-dashboard', views.donor_dashboard_view,name='donor-dashboard'),
    path('donate-blood', views.donate_blood_view,name='donate-blood'),
    path('donation-history', views.donation_history_view,name='donation-history'),
    path('make-request', views.make_request_view,name='make-request'),
    path('request-history', views.request_history_view,name='request-history'),


]
