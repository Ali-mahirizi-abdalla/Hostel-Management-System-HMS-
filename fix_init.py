
import os

files = [
    r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\management\__init__.py",
    r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\management\commands\__init__.py"
]

for path in files:
    print(f"fixing {path}")
    with open(path, 'w', encoding='utf-8') as f:
        f.write("")
    print("Done.")
