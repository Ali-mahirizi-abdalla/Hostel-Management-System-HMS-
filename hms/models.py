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
