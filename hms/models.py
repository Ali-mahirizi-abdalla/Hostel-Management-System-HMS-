from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta


class StudentProfile(models.Model):
    """Extended profile for students with hostel-specific information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    room_number = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, blank=True)
    is_away = models.BooleanField(default=False)
    away_from_date = models.DateField(null=True, blank=True)
    away_to_date = models.DateField(null=True, blank=True)
    default_early_breakfast = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['room_number']

    def __str__(self):
        return f"{self.user.get_full_name()} - Room {self.room_number}"

    def mark_away(self, from_date, to_date):
        """Mark student as away and auto-set meals to No"""
        self.is_away = True
        self.away_from_date = from_date
        self.away_to_date = to_date
        self.save()
        
        # Auto-create meal confirmations with all meals set to False
        current_date = from_date
        while current_date <= to_date:
            MealConfirmation.objects.update_or_create(
                student=self,
                date=current_date,
                defaults={
                    'breakfast': False,
                    'lunch': False,
                    'supper': False,
                    'early_breakfast_needed': False
                }
            )
            current_date += timedelta(days=1)

    def mark_return(self):
        """Mark student as returned"""
        self.is_away = False
        self.away_from_date = None
        self.away_to_date = None
        self.save()


class MealConfirmation(models.Model):
    """Daily meal confirmation for each student"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='meal_confirmations')
    date = models.DateField()
    breakfast = models.BooleanField(default=True)
    lunch = models.BooleanField(default=True)
    supper = models.BooleanField(default=True)
    early_breakfast_needed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date', 'student__room_number']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.date}"

    @classmethod
    def get_meal_count(cls, meal_date, meal_type='breakfast'):
        """Get count of students taking a specific meal on a date"""
        confirmations = cls.objects.filter(date=meal_date)
        
        if meal_type == 'breakfast':
            return confirmations.filter(breakfast=True).count()
        elif meal_type == 'lunch':
            return confirmations.filter(lunch=True).count()
        elif meal_type == 'supper':
            return confirmations.filter(supper=True).count()
        return 0

    @classmethod
    def get_early_breakfast_count(cls, meal_date):
        """Get count of students needing early breakfast"""
        return cls.objects.filter(
            date=meal_date,
            breakfast=True,
            early_breakfast_needed=True
        ).count()

    @classmethod
    def get_early_breakfast_students(cls, meal_date):
        """Get list of students needing early breakfast"""
        return cls.objects.filter(
            date=meal_date,
            breakfast=True,
            early_breakfast_needed=True
        ).select_related('student__user')


class ActivitySchedule(models.Model):
    """Weekly recurring activities that may affect meal timing"""
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    activity_name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    affects_meal_timing = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.get_day_of_week_display()} - {self.activity_name}"


class Announcement(models.Model):
    """System announcements for students"""
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class MealTimingOverride(models.Model):
    """Override meal timing for specific dates"""
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('supper', 'Supper'),
    ]

    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    custom_time = models.TimeField()
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['date', 'meal_type']
        ordering = ['date', 'meal_type']

    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.date} at {self.custom_time}"
