from django.contrib.auth.views import LogoutView,LoginView
from django.urls import path
from blood import views


urlpatterns = [
    
    path('home',views.home_view,name='home'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('adminlogin', LoginView.as_view(template_name='blood/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('logout', LogoutView.as_view(template_name='blood/logout.html'),name='logout'),
]

