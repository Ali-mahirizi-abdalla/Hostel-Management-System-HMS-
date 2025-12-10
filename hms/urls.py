from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'hms'

urlpatterns = [
    # Authentication
    path('', views.user_login, name='home'),
    path('register/', views.register_student, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Student
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/confirm-meals/', views.confirm_meals, name='confirm_meals'),
    path('student/toggle-away/', views.toggle_away_mode, name='toggle_away'),
    path('student/early-breakfast/', views.toggle_early_breakfast, name='toggle_early_breakfast'),
    
    # Kitchen / Admin
    path('kitchen/dashboard/', views.dashboard_admin, name='admin_dashboard'),
    path('kitchen/export-csv/', views.export_meals_csv, name='export_meals_csv'),
    
    # Password Reset
    # Explicitly defining these to ensure they are available
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='hms/registration/password_reset_form.html',
             email_template_name='hms/registration/password_reset_email.html',
             success_url=reverse_lazy('hms:password_reset_done')
         ), 
         name='password_reset'),
         
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='hms/registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
         
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='hms/registration/password_reset_confirm.html',
             success_url=reverse_lazy('hms:password_reset_complete')
         ), 
         name='password_reset_confirm'),
         
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='hms/registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]