from django.urls import path
from. import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),  
    path('login/', views.login_view, name='login'),  
    path('accounts/login/', views.login_view, name='login_accounts'),  
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'), 
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'), 
    path('', views.home, name='home'),  
    path('create_blog_post/', views.create_blog_post, name='create_blog_post'), 
]
