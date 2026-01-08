import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hostel_System.settings')
django.setup()

from django.contrib.auth.models import User
from hms.models import Student

print("--- Users ---")
for user in User.objects.all():
    print(f"Username: {user.username}, Email: {user.email}, Active: {user.is_active}")
    if hasattr(user, 'student_profile'):
        print(f"  - Student Profile: Room {user.student_profile.room_number}")
    else:
        print("  - No Student Profile")

print("\n--- End ---")
