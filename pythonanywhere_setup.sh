#!/bin/bash

# PythonAnywhere Setup Script
# Run this script in the PythonAnywhere Bash console

echo "🚀 Starting PythonAnywhere Setup..."

# 1. Detect Environment
HOME_DIR=$(pwd)
USERNAME=$(whoami)
PROJECT_DIR="$HOME_DIR/Hostel_System"

echo "📍 Home Directory: $HOME_DIR"
echo "👤 Username: $USERNAME"

# 2. Pull Latest Code
if [ -d "$PROJECT_DIR" ]; then
    echo "📂 Project directory exists. Pulling latest changes..."
    cd "$PROJECT_DIR"
    git pull
else
    echo "📂 Cloning repository..."
    # Note: You might need to update this URL if it's different
    git clone https://github.com/Alimahirizi/Hostel-Management-System-HMS-.git "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# 3. Setup Virtual Environment
echo "🐍 Setting up Virtual Environment..."
if [ ! -d "$HOME_DIR/.virtualenvs/hostelenv" ]; then
    mkvirtualenv --python=/usr/bin/python3.10 hostelenv
else
    workon hostelenv
fi

# 4. Install Requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# 5. Configure Settings
echo "⚙️ Configuring Django Settings..."
SETTINGS_FILE="$PROJECT_DIR/Hostel_System/settings.py"
sed -i "s/DEBUG = True/DEBUG = False/" "$SETTINGS_FILE"
sed -i "s/ALLOWED_HOSTS = .*/ALLOWED_HOSTS = ['*']/" "$SETTINGS_FILE"

# 6. Database Migrations
echo "🗄️ Running Migrations..."
python manage.py migrate

# 7. Collect Static Files
echo "🎨 Collecting Static Files..."
python manage.py collectstatic --noinput

# 8. Create Superuser (Interactive)
echo "👤 Create Superuser (Optional - press Ctrl+C to skip if already created)"
python manage.py createsuperuser

echo "✅ Setup Complete!"
echo "⚠️  IMPORTANT: Don't forget to configure the WSGI file in the Web tab!"
