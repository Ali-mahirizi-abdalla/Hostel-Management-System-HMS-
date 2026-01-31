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
    path('manage/activities/create/', views.create_activity, name='create_activity'),
    path('manage/activities/edit/<int:pk>/', views.edit_activity, name='edit_activity'),
    path('manage/activities/delete/<int:pk>/', views.delete_activity, name='delete_activity'),
    path('manage/activities/toggle/<int:pk>/', views.toggle_activity_status, name='toggle_activity_status'),

    # Features
    path('manage/upload-document/', views.upload_document, name='upload_document'),
    path('student/upload-timetable/', views.upload_timetable, name='upload_timetable'),
    path('student/select-room/', views.select_room, name='select_room'),
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:recipient_id>/', views.chat_view, name='chat_with'),

    # Maintenance
    path('student/maintenance/', views.student_maintenance_list, name='student_maintenance_list'),
    path('student/maintenance/create/', views.submit_maintenance_request, name='submit_maintenance_request'),
    path('student/maintenance/delete/<int:pk>/', views.delete_maintenance_request, name='delete_maintenance_request'),
    path('manage/maintenance/', views.manage_maintenance, name='manage_maintenance'),
    path('manage/maintenance/update/<int:pk>/', views.update_maintenance_status, name='update_maintenance_status'),

    # Leave Requests
    path('student/leave/', views.student_leave_list, name='student_leave_list'),
    path('student/leave/create/', views.submit_leave_request, name='submit_leave_request'),
    path('student/leave/delete/<int:pk>/', views.delete_leave_request, name='delete_leave_request'),
    path('manage/leave/', views.manage_leave_requests, name='manage_leave_requests'),
    path('manage/leave/approve/<int:pk>/', views.approve_leave_request, name='approve_leave_request'),

    # Room Management
    path('manage/rooms/', views.room_list, name='room_list'),
    path('manage/rooms/create/', views.create_room, name='create_room'),
    path('manage/rooms/edit/<int:pk>/', views.edit_room, name='edit_room'),
    path('manage/rooms/delete/<int:pk>/', views.delete_room, name='delete_room'),
    path('manage/rooms/assignments/', views.room_assignments, name='room_assignments'),
    path('manage/rooms/assign/', views.assign_room, name='assign_room'),
    path('manage/rooms/change-requests/', views.room_change_requests, name='room_change_requests'),
    path('manage/rooms/change-requests/approve/<int:pk>/', views.approve_room_change, name='approve_room_change'),
    path('student/room-change/', views.student_request_room_change, name='student_request_room_change'),

    # Analytics Dashboard
    path('manage/analytics/', views.analytics_dashboard, name='analytics_dashboard'),

    # Visitor Management
    path('manage/visitors/', views.visitor_management, name='visitor_management'),
    path('manage/visitors/checkout/<int:visitor_id>/', views.checkout_visitor, name='checkout_visitor'),

    # Event Management
    path('events/', views.events_list, name='events_list'),
    path('events/my-rsvps/', views.my_events, name='my_events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/rsvp/', views.event_rsvp, name='event_rsvp'),
    path('manage/events/', views.manage_events, name='manage_events'),
    path('manage/events/create/', views.create_event, name='create_event'),
    path('manage/events/edit/<int:pk>/', views.edit_event, name='edit_event'),
    path('manage/events/delete/<int:pk>/', views.delete_event, name='delete_event'),
    path('manage/events/<int:pk>/attendees/', views.event_attendees, name='event_attendees'),


    
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
    # Payment / M-Pesa
    path('student/pay-accommodation/', views.pay_accommodation, name='pay_accommodation'),
    path('student/payment-history/', views.payment_history, name='payment_history'),
    path('payment/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('payment/check/<int:payment_id>/', views.check_payment_status, name='check_payment_status'),
]