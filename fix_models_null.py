
import os

files = [
    r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\models.py",
    r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\signals.py",
    r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\middleware.py",
    r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\admin.py",
    r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\management\commands\send_meal_reminders.py",
    r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\Hostel_System\settings.py"
]

for path in files:
    print(f"Checking {path}...")
    try:
        with open(path, 'rb') as f:
            content = f.read()

        if b'\x00' in content:
            print(f"Found null bytes in {path}! Removing them.")
            content = content.replace(b'\x00', b'')
            with open(path, 'wb') as f:
                f.write(content)
            print("Fixed.")
        else:
            print("Clean.")
    except Exception as e:
        print(f"Error checking {path}: {e}")
