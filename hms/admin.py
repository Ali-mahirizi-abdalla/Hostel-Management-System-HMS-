from django.contrib import admin
from .models import Student, Meal, Activity, AwayPeriod

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'university_id', 'phone', 'is_warden')
    search_fields = ('user__username', 'university_id', 'phone')

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'breakfast', 'early', 'supper', 'away')
    list_filter = ('date', 'breakfast', 'supper', 'away')
    search_fields = ('student__user__username', 'student__university_id')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'weekday', 'time', 'active')
    list_filter = ('weekday', 'active')

@admin.register(AwayPeriod)
class AwayPeriodAdmin(admin.ModelAdmin):
    list_display = ('student', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')