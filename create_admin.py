from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hostel_System.settings')
django.setup()

User = get_user_model()

def create_admin():
    username = 'mahrez'
    email = 'alimahrez744@gmail.com'
    password = 'A8486aom'
    
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print(f"Superuser {username} already exists.")

if __name__ == '__main__':
    create_admin()
