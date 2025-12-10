#!/usr/bin/env python
import os
import sys

def main():
    print("="*50)
    print("DEBUG: manage.py starting check")
    
    # 1. Determine correct project root (preferring CWD to avoid symlink confusion)
    cwd = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if os.path.exists(os.path.join(cwd, 'manage.py')):
        project_root = cwd
        print(f"DEBUG: Using CWD as project root: {project_root}")
    else:
        project_root = script_dir
        print(f"DEBUG: Using Script Dir as project root: {project_root}")

    # 2. Aggressively clean sys.path to remove conflicting entries
    cleaned_path = []
    conflict_marker = 'Hostel-Management-System-HMS--master'
    
    for p in sys.path:
        p_str = str(p)
        if conflict_marker in p_str:
             print(f"DEBUG: Removing conflicting path from sys.path: {p_str}")
             continue
        cleaned_path.append(p)
    sys.path = cleaned_path

    # 3. Insert correct project root
    sys.path.insert(0, project_root)
    print(f"DEBUG: sys.path[0] enforced to: {sys.path[0]}")
    print("="*50)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hostel_System.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
