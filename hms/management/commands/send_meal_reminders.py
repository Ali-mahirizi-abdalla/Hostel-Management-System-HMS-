from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from hms.models import Notification
import datetime

class Command(BaseCommand):
    help = 'Send meal reminders to students based on current time'

    def handle(self, *args, **kwargs):
        now = timezone.localtime(timezone.now())
        current_time = now.time()
        
        meal_type = None
        
        # Define ranges (adjust as per hostel rules)
        # Breakfast: 6:00 AM - 9:00 AM
        if datetime.time(6, 0) <= current_time <= datetime.time(9, 0):
            meal_type = 'Breakfast'
        # Lunch: 11:00 AM - 2:00 PM
        elif datetime.time(11, 0) <= current_time <= datetime.time(14, 0):
            meal_type = 'Lunch'
        # Dinner: 5:00 PM - 8:00 PM
        elif datetime.time(17, 0) <= current_time <= datetime.time(20, 0):
            meal_type = 'Dinner'
            
        if not meal_type:
            self.stdout.write(self.style.WARNING(f'No active meal time found at {current_time}.'))
            return

        # Get all students
        users = User.objects.filter(student_profile__isnull=False)
        count = 0
        
        for user in users:
            # Prevent duplicate notifications for same meal on same day could be added here
            # For now, we assume this command runs once per meal slot
            Notification.objects.create(
                user=user,
                title=f"🍽️ {meal_type} is Ready!",
                message=f"Don't forget to have your {meal_type}. The mess hall is open.",
                link="/student/dashboard/"
            )
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully sent {count} {meal_type} reminders.'))
