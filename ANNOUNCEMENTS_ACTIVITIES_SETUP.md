# Announcements and Activities Setup

## Summary
Successfully added announcements and activities functionality to the Hostel Management System.

## Changes Made

### 1. Models (`hms/models.py`)
Added `Announcement` model with the following fields:
- `title`: CharField (max 200 characters)
- `content`: TextField
- `created_by`: ForeignKey to User
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)
- `is_active`: BooleanField (default True)
- `priority`: CharField with choices (low, normal, high, urgent)

### 2. Views (`hms/views.py`)
Added the following views:
- `announcements_list()`: View all active announcements
- `manage_announcements()`: Admin page to create/delete announcements
- `create_announcement()`: Create new announcement form
- `activities_list()`: View all active activities

### 3. URLs (`hms/urls.py`)
Added URL patterns:
- `/announcements/` - View announcements (all users)
- `/admin/announcements/` - Manage announcements (admin only)
- `/admin/announcements/create/` - Create announcement form (admin only)
- `/admin/activities/` - View activities (admin only)

### 4. Admin Panel (`hms/admin.py`)
Registered `Announcement` model in Django admin with:
- List display: title, priority, is_active, created_by, created_at
- Filters: priority, is_active, created_at
- Search: title, content

## Available Pages

### For All Users:
- **Announcements**: `http://localhost:8000/announcements/`

### For Admin Only:
- **Manage Announcements**: `http://localhost:8000/admin/announcements/`
- **Create Announcement**: `http://localhost:8000/admin/announcements/create/`
- **Activities**: `http://localhost:8000/admin/activities/`

## Templates
The following templates are already available and will work with the new views:
- `hms/admin/announcements.html`
- `hms/admin/manage_announcements.html`
- `hms/admin/announcement_form.html`
- `hms/admin/activities.html`

## How to Use

### Creating an Announcement (Admin):
1. Navigate to `/admin/announcements/`
2. Click "Create New Announcement" or use the form
3. Fill in title, content, and priority
4. Submit to create

### Viewing Announcements (Students):
1. Navigate to `/announcements/`
2. See all active announcements ordered by date

### Managing Activities (Admin):
1. Navigate to `/admin/activities/`
2. View all weekly activities
3. Can add/edit via Django admin panel at `/admin/`

## Database
The `Announcement` model has been added to the database. If you need to create the table manually, run:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Next Steps
You can now access these pages from your admin dashboard by adding navigation links to the sidebar or header.
