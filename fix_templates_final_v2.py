
import os

def fix_base_html():
    file_path = os.path.join('hms', 'templates', 'hms', 'base.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The target string to fix
    # We are looking for the split template tag
    old_fragment = '{% if user.is_staff %}Admin{%\n                            else %}Student{% endif %}'
    new_fragment = '{% if user.is_staff %}Admin{% else %}Student{% endif %}'
    
    # Try normalizing line endings just in case
    # content = content.replace('\r\n', '\n') 
    
    if old_fragment in content:
        print("Found split tag in base.html. Fixing...")
        new_content = content.replace(old_fragment, new_fragment)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Fixed base.html")
    else:
        # Fallback: try manual search if exact match fails due to whitespace
        print("Exact match failed for base.html, trying looser match...")
        lines = content.splitlines()
        new_lines = []
        skip_next = False
        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
            
            if '{% if user.is_staff %}Admin{%' in line and i + 1 < len(lines) and 'else %}Student{% endif %}' in lines[i+1]:
                print(f"Found split lines at {i+1} and {i+2}")
                # Construct the combined line, preserving indentation of the first line
                start_part = line.split('{%')[0]
                combined = start_part + '{% if user.is_staff %}Admin{% else %}Student{% endif %}</p>'
                new_lines.append(combined)
                # Skip the next line as it's merged
                skip_next = True
            else:
                new_lines.append(line)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print("Fixed base.html (method 2)")

def fix_announcements_html():
    file_path = os.path.join('hms', 'templates', 'hms', 'admin', 'manage_announcements.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixed_content = content.replace("status_filter=='active'", "status_filter == 'active'")
    fixed_content = fixed_content.replace("status_filter=='inactive'", "status_filter == 'inactive'")
    
    if fixed_content != content:
        print("Fixing manage_announcements.html...")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print("Fixed manage_announcements.html")
    else:
        print("No changes needed for manage_announcements.html (or match failed)")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    print(f"Working directory: {os.getcwd()}")
    
    try:
        fix_base_html()
    except Exception as e:
        print(f"Error fixing base.html: {e}")
        
    try:
        fix_announcements_html()
    except Exception as e:
        print(f"Error fixing manage_announcements.html: {e}")
