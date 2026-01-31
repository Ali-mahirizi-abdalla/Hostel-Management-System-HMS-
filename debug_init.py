
path = r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\management\__init__.py"
try:
    with open(path, 'rb') as f:
        print(f"Content: {f.read()}")
except Exception as e:
    print(f"Error: {e}")
