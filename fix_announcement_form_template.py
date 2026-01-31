
import os

file_path = r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\templates\hms\admin\announcement_form.html"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the problematic strings
content = content.replace("announcement.priority=='low'", "announcement.priority == 'low'")
content = content.replace("announcement.priority=='normal'", "announcement.priority == 'normal'")
content = content.replace("announcement.priority=='high'", "announcement.priority == 'high'")
content = content.replace("announcement.priority=='urgent'", "announcement.priority == 'urgent'")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed {file_path}")
