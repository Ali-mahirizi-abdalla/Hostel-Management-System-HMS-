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
    path('kitchen/send-notifications/', views.send_meal_notifications, name='send_notifications'),
    
    # Student Management
    path('manage/students/', views.manage_students, name='manage_students'),
    path('manage/students/add/', views.add_student, name='add_student'),
    path('manage/students/edit/<int:user_id>/', views.edit_student, name='edit_student'),
    path('manage/students/delete/<int:user_id>/', views.delete_student, name='delete_student'),
    path('manage/students/details/<int:user_id>/', views.student_details, name='student_details'),
    path('manage/away-list/', views.away_list, name='away_list'),
    
    # Announcements
    path('announcements/', views.announcements_list, name='announcements'),
    path('manage/announcements/', views.manage_announcements, name='manage_announcements'),
    path('manage/announcements/create/', views.create_announcement, name='create_announcement'),
    path('manage/announcements/edit/<int:pk>/', views.edit_announcement, name='edit_announcement'),
    path('manage/announcements/delete/<int:pk>/', views.delete_announcement, name='delete_announcement'),
    
    # Activities
    path('manage/activities/', views.activities_list, name='activities'),

    # Features
    path('manage/upload-document/', views.upload_document, name='upload_document'),
    path('student/upload-timetable/', views.upload_timetable, name='upload_timetable'),
    path('student/select-room/', views.select_room, name='select_room'),
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:recipient_id>/', views.chat_view, name='chat_with'),

    
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