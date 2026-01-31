#!/usr/bin/env python
# Fix Django template syntax errors in maintenance_list.html

import sys

# Read the file
with open('hms/templates/hms/admin/maintenance_list.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the syntax errors - add spaces around ==
content = content.replace("req.status=='pending'", "req.status == 'pending'")
content = content.replace("req.status=='in_progress'", "req.status == 'in_progress'")
content = content.replace("req.status=='resolved'", "req.status == 'resolved'")

# Write back
with open('hms/templates/hms/admin/maintenance_list.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed Django template syntax errors")
print("  - Added spaces around == operators")
print("  - File: hms/templates/hms/admin/maintenance_list.html")
