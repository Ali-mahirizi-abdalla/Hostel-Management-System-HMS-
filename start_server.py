import os
import sys

def main():
    print("="*50)
    print("DEBUG: start_server.py launching...")
    
    # 1. Force the current directory (where this script is) to be the project root
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"DEBUG: Enforcing base_dir: {base_dir}")
    
    # 2. Build a clean sys.path
    # Keep standard library paths, but Filter out any suspicious project paths
    new_sys_path = []
    conflict_marker = 'Hostel-Management-System-HMS--master'
    
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
        
    for p in sys.path:
        p_str = str(p)
        # Remove paths that match the conflict marker UNLESS it matches our base_dir 
        # (in case base_dir happens to be inside such a path, though unlikely given the context)
        if conflict_marker in p_str and base_dir not in p_str:
            print(f"DEBUG: Removing conflicting path: {p_str}")
            continue
        new_sys_path.append(p)
    
    sys.path = new_sys_path
    
    # Ensure base_dir is first
    if base_dir in sys.path:
        sys.path.remove(base_dir)
    sys.path.insert(0, base_dir)
    
    print(f"DEBUG: sys.path[0]: {sys.path[0]}")
    print("="*50)

    # 3. Configure settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hostel_System.settings")
    
    # 4. Execute
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver'])

if __name__ == "__main__":
    main()
