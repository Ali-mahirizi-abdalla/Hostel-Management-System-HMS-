from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Student(models.Model):
    """Extended profile for students"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    university_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    timetable = models.FileField(upload_to='timetables/', blank=True, null=True)
    room_number = models.CharField(max_length=10, blank=True, null=True)
    is_warden = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.university_id})"

class Meal(models.Model):
    """Daily meal submission"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='meals')
    date = models.DateField(default=timezone.now)
    breakfast = models.BooleanField(default=False)
    early = models.BooleanField(default=False) # Early breakfast
    supper = models.BooleanField(default=False)
    away = models.BooleanField(default=False) # Check if marked away for this specific day
    submitted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.date}"

class AwayPeriod(models.Model):
    """Periods when a student is away"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='away_periods')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return f"{self.student} Away: {self.start_date} to {self.end_date}"

class Activity(models.Model):
    """Weekly activities"""
    display_name = models.CharField(max_length=100)
    weekday = models.IntegerField(choices=[
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
    ])
    description = models.TextField(blank=True)
    time = models.TimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['weekday', 'time']

    def __str__(self):
        return f"{self.get_weekday_display()} - {self.display_name}"

class Announcement(models.Model):
    """System announcements"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='normal')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Document(models.Model):
    """Admin uploaded documents for students"""
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Message(models.Model):
    """Chat messages between student and admin"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender} to {self.recipient}"


class MaintenanceRequest(models.Model):
    """Maintenance tickets submitted by students"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='maintenance_requests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='maintenance_photos/', blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.student} ({self.get_status_display()})"


class Room(models.Model):
    """Hostel room information"""
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('quad', 'Quad'),
    ]
    
    room_number = models.CharField(max_length=10, unique=True)
    floor = models.IntegerField()
    block = models.CharField(max_length=50, blank=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='double')
    capacity = models.IntegerField(default=2)
    is_available = models.BooleanField(default=True)
    amenities = models.TextField(blank=True, help_text="List amenities (e.g., AC, attached bathroom)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['block', 'floor', 'room_number']
    
    def __str__(self):
        return f"Room {self.room_number} - {self.get_room_type_display()}"
    
    @property
    def current_occupancy(self):
        """Get current number of students in the room"""
        return self.assignments.filter(is_active=True).count()
    
    @property
    def available_beds(self):
        """Get number of available beds"""
        return self.capacity - self.current_occupancy


class RoomAssignment(models.Model):
    """Track room assignments for students"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='room_assignments')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='assignments')
    bed_number = models.IntegerField(null=True, blank=True)
    assigned_date = models.DateField(default=timezone.now)
    checkout_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-assigned_date']
    
    def __str__(self):
        return f"{self.student} - {self.room} (Bed {self.bed_number})"


class RoomChangeRequest(models.Model):
    """Student requests for room changes"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='room_change_requests')
    current_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='change_requests_from')
    requested_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='change_requests_to')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_room_changes')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student} - Room Change Request ({self.get_status_display()})"


class LeaveRequest(models.Model):
    """Leave applications from students"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    LEAVE_TYPES = [
        ('home', 'Going Home'),
        ('medical', 'Medical Leave'),
        ('emergency', 'Emergency'),
        ('other', 'Other'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES, default='home')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    contact_during_leave = models.CharField(max_length=15, blank=True, help_text="Phone number during leave")
    destination = models.CharField(max_length=200, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_leaves')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student} - Leave ({self.start_date} to {self.end_date})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")
    
    @property
    def duration_days(self):
        """Calculate leave duration in days"""
        return (self.end_date - self.start_date).days + 1


class Visitor(models.Model):
    """Visitor logbook for hostel security"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='visitors')
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, blank=True)
    id_number = models.CharField(max_length=50, blank=True, help_text="National ID or Passport Number")
    
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(null=True, blank=True)
    purpose = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='registered_visitors')
    
    class Meta:
        ordering = ['-check_in_time']
    
    def __str__(self):
        return f"{self.name} visiting {self.student}"
    
    def check_out(self):
        self.check_out_time = timezone.now()
        self.is_active = False
        self.save()
