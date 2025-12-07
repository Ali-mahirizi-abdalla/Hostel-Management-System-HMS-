import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hostel_System.settings')
django.setup()

from django.contrib.auth.models import User

username = 'issa'
try:
    user = User.objects.get(username=username)
    user.set_password('password123')
    user.save()
    print(f"Successfully reset password for '{username}' to 'password123'")
except User.DoesNotExist:
    print(f"User '{username}' not found.")
