from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('patientlogin/', LoginView.as_view(template_name='patient/patientlogin.html'), name='patientlogin'),
    path('patientsignup/', views.patient_signup_view, name='patientsignup'),
    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),

]
