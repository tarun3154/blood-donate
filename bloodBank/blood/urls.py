from django.contrib.auth.views import LogoutView,LoginView
from django.urls import path
from blood import views


urlpatterns = [
    
    path('home',views.home_view,name='home'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('adminlogin', LoginView.as_view(template_name='blood/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-donor', views.admin_donor_view,name='admin-donor'),
    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('update-donor/<int:pk>', views.update_donor_view,name='update-donor'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('delete-donor/<int:pk>', views.delete_donor_view,name='delete-donor'),
    path('delete-patient/<int:pk>', views.delete_patient_view,name='delete-patient'),
    path('admin-request', views.admin_request_view,name='admin-request'),
    path('admin-request-history', views.admin_request_history_view,name='admin-request-history'),
    path('admin-donation', views.admin_donation_view,name='admin-donation'),
    path('approve-donation/<int:pk>', views.approve_donation_view,name='approve-donation'),
    path('reject-donation/<int:pk>', views.reject_donation_view,name='reject-donation'),

    path('logout', LogoutView.as_view(template_name='blood/logout.html'),name='logout'),
]

