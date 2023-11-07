from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('patientsignup/', views.patient_signup_view, name='patientsignup'),
    path('patientlogin/', LoginView.as_view(template_name='patient/patientlogin.html'), name='patientlogin'),
    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('make-requests', views.make_request_view,name='make-requests'),
    path('my-request', views.my_request_view,name='my-request'),
]
