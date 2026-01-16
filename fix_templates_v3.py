
import os
import re

def fix_variable_tags():
    file_path = os.path.join('hms', 'templates', 'hms', 'admin', 'manage_announcements.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to find {{ ... }} blocks that span multiple lines and join them.
    # Pattern: {{ followed by anything (non-greedy) including newlines, until }}
    # But only if it contains a newline.
    
    pattern = re.compile(r'\{\{\s*?\n(.*?)\n\s*?\}\}', re.DOTALL)
    
    matches = pattern.findall(content)
    if matches:
        print(f"Found {len(matches)} multi-line variable tags. Fixing...")
        
        def replacement(match):
            # Extract the inner content, strip whitespace/newlines, and wrap back in {{ }}
            inner = match.group(1)
            # Replace newlines with spaces or just strip
            clean_inner = ' '.join(inner.split())
            return f"{{{{ {clean_inner} }}}}"
            
        new_content = pattern.sub(replacement, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Fixed multi-line variable tags in manage_announcements.html")
    else:
        print("No multi-line variable tags found matching the pattern.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    try:
        fix_variable_tags()
    except Exception as e:
        print(f"Error: {e}")
