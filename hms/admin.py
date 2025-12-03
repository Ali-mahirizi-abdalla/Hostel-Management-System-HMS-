from django.contrib import admin
from .models import StudentProfile, MealConfirmation, ActivitySchedule, Announcement, MealTimingOverride


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'room_number', 'phone_number', 'is_away', 'away_from_date', 'away_to_date']
    list_filter = ['is_away', 'default_early_breakfast']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'room_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MealConfirmation)
class MealConfirmationAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'breakfast', 'lunch', 'supper', 'early_breakfast_needed', 'confirmed_at']
    list_filter = ['date', 'breakfast', 'lunch', 'supper', 'early_breakfast_needed']
    search_fields = ['student__user__username', 'student__user__first_name', 'student__user__last_name']
    date_hierarchy = 'date'


@admin.register(ActivitySchedule)
class ActivityScheduleAdmin(admin.ModelAdmin):
    list_display = ['day_of_week', 'activity_name', 'start_time', 'end_time', 'affects_meal_timing', 'is_active']
    list_filter = ['day_of_week', 'is_active', 'affects_meal_timing']
    search_fields = ['activity_name']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'created_by', 'created_at', 'is_active']
    list_filter = ['priority', 'is_active', 'created_at']
    search_fields = ['title', 'message']
    readonly_fields = ['created_at']


@admin.register(MealTimingOverride)
class MealTimingOverrideAdmin(admin.ModelAdmin):
    list_display = ['date', 'meal_type', 'custom_time', 'reason']
    list_filter = ['meal_type', 'date']
    date_hierarchy = 'date'