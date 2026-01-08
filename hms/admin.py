from django.contrib import admin
from .models import (Student, Meal, Activity, AwayPeriod, Announcement, 
                     MaintenanceRequest, Room, RoomAssignment, RoomChangeRequest, LeaveRequest)

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

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'is_active', 'created_by', 'created_at')
    list_filter = ('priority', 'is_active', 'created_at')
    search_fields = ('title', 'content')


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'priority', 'status', 'created_at')
    list_filter = ('priority', 'status', 'created_at')
    search_fields = ('title', 'description', 'student__user__username')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'floor', 'block', 'room_type', 'capacity', 'current_occupancy', 'is_available')
    list_filter = ('floor', 'block', 'room_type', 'is_available')
    search_fields = ('room_number', 'block')


@admin.register(RoomAssignment)
class RoomAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'bed_number', 'assigned_date', 'is_active')
    list_filter = ('is_active', 'assigned_date')
    search_fields = ('student__user__username', 'room__room_number')


@admin.register(RoomChangeRequest)
class RoomChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'current_room', 'requested_room', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('student__user__username', 'reason')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'leave_type', 'start_date', 'end_date', 'status', 'duration_days')
    list_filter = ('leave_type', 'status', 'start_date')
    search_fields = ('student__user__username', 'reason', 'destination')
