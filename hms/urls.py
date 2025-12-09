from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'hms'

urlpatterns = [
    # Authentication
    path('', views.student_dashboard, name='home'),
    path('register/', views.register_student, name='register'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/confirm-meals/', views.confirm_meals, name='confirm_meals'),
    path('student/toggle-away/', views.toggle_away_mode, name='toggle_away'),
    path('student/early-breakfast/', views.toggle_early_breakfast, name='toggle_early_breakfast'),
    path('student/profile/', views.student_profile, name='student_profile'),
    
    # Kitchen URLs
    path('kitchen/dashboard/', views.kitchen_dashboard, name='kitchen_dashboard'),
    path('kitchen/meal-count-api/', views.meal_count_api, name='meal_count_api'),
    path('kitchen/early-breakfast-list/', views.early_breakfast_list, name='early_breakfast_list'),
    path('kitchen/daily-report/', views.daily_report, name='daily_report'),
    path('kitchen/export-csv/', views.export_meals_csv, name='export_meals_csv'),
    
    # Admin/Warden URLs
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/activities/', views.manage_activities, name='manage_activities'),
    path('admin-panel/announcements/', views.manage_announcements, name='manage_announcements'),
    path('admin-panel/students/', views.manage_students, name='manage_students'),
    
    # Password reset URLs
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='hms/registration/password_reset_form.html',
             email_template_name='hms/registration/password_reset_email.html',
             subject_template_name='hms/registration/password_reset_subject.txt',
             success_url=reverse_lazy('hms:password_reset_done')
         ), 
         name='password_reset'),
    path('password_reset/done/', 
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