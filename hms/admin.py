from django.contrib import admin
from .models import (Student, Meal, Activity, AwayPeriod, Announcement, 
                     MaintenanceRequest, Room, RoomAssignment, RoomChangeRequest, LeaveRequest,
                     Event, EventRSVP, LoginActivity, AuditLog, Notification, Payment)

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

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'event_date', 'start_time', 'rsvp_count', 'is_published')
    list_filter = ('category', 'is_published', 'event_date', 'is_mandatory')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'event_date'

@admin.register(EventRSVP)
class EventRSVPAdmin(admin.ModelAdmin):
    list_display = ('event', 'student', 'status', 'attended', 'created_at')
    list_filter = ('status', 'attended', 'event')
    search_fields = ('event__title', 'student__user__username', 'student__university_id')

@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'timestamp', 'status')
    list_filter = ('timestamp', 'status')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('user', 'ip_address', 'user_agent', 'timestamp', 'status')

    def has_add_permission(self, request):
        return False

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'model_name', 'object_repr', 'user', 'timestamp')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('object_repr', 'changes', 'user__username')
    readonly_fields = ('user', 'model_name', 'object_id', 'object_repr', 'action', 'changes', 'timestamp')

    def has_add_permission(self, request):
        return False
        
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'transaction_id', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('student__user__username', 'transaction_id', 'phone_number')
    readonly_fields = ('transaction_id', 'checkout_request_id', 'created_at')
