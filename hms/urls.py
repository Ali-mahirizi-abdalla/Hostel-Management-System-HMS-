from django.urls import path
from . import views

app_name = 'hms'

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
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
    
    # Admin/Warden URLs
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/activities/', views.manage_activities, name='manage_activities'),
    path('admin-panel/announcements/', views.manage_announcements, name='manage_announcements'),
    path('admin-panel/students/', views.manage_students, name='manage_students'),
]
