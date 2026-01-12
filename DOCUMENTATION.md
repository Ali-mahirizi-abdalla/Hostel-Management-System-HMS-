# Hostel Management System (HMS) Documentation

## 1. Introduction
The **Hostel Management System (HMS)** is a robust, web-based application designed to digitize and streamline the day-to-day operations of managing a student hostel. It provides a seamless interface for both students and administrators to handle accommodation, meals, maintenance, and communication.

## 2. Technology Stack
- **Backend Framework:** Django (Python)
- **Database:** SQLite (Development) / PostgreSQL (Production supported)
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **Authentication:** Django Auth System + `django-allauth` (Google OAuth supported)
- **Deployment:** Ready for platforms like Render or Vercel (includes `build.sh`, `render.yaml`)

## 3. Key Features

###For Students
- **Dashboard:** A central hub showing announcements, daily meal status, and quick actions.
- **Profile Management:** updates to personal info, profile picture upload, and university timetable upload.
- **Room Management:** 
    - View available rooms.
    - Select specific rooms/beds based on real-time availability.
    - Request room changes.
- **Meal Management:**
    - Book meals (Breakfast, Early Breakfast, Supper) for today and tomorrow.
    - **Away Mode:** Mark yourself as "Away" for a date range to automatically opt-out of meals.
- **Services:**
    - **Maintenance:** Report issues (e.g., plumbing, electrical) with photos and track repair status.
    - **Leave Requests:** Apply for leave (home, medical, etc.) and track approval status.
- **Communication:** Direct chat interface with hostel administration.

### For Administrators (Wardens/Staff)
- **Admin Dashboard:** Analytics on meal consumption, room occupancy, pending requests, and system health.
- **Student Management:** View, add, edit, or remove student profiles.
- **Room Management:**
    - Create and configure rooms (Capacity, Floor, Block, Type).
    - Manage room assignments and handle change requests.
    - View occupancy rates.
- **Mess/Kitchen Management:**
    - View daily meal counts.
    - Export meal data to CSV for kitchen staff.
    - Send notifications to students who haven't booked.
- **Requests Oversight:**
    - Approve/Reject leave requests (automatically updates "Away Mode").
    - Update status of maintenance tickets (e.g., Pending -> In Progress -> Resolved).
- **Visitor Management:** Log and track visitors entering/exiting the premises.
- **Announcements:** Post system-wide updates for students.

## 4. Database Models (Core)
- **Student:** Extends the user model with university ID, phone, profile pic, etc.
- **Room:** Stores room number, capacity, type (Single/Double), and availability status.
- **RoomAssignment:** Links a Student to a Room.
- **Meal:** Tracks daily meal choices per student.
- **AwayPeriod:** Stores dates when a student is away (disables meals).
- **MaintenanceRequest:** Tickets with priority, status, and image.
- **LeaveRequest:** structured leave applications with approval workflow.
- **Visitor:** Logs visitor details and time in/out.

## 5. Installation & Setup Guide

### Prerequisites
- Python 3.8+ installed.
- Git.

### Step-by-Step Setup

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd Hostel-Management-System-HMS-
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Database Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    # Follow the prompts to set username/password
    ```

6.  **Run the Server**
    ```bash
    python manage.py runserver
    ```
    Access the app at: `http://127.0.0.1:8000/`

## 6. Project Structure
- `Hostel_System/`: Main Django project configuration (`settings.py`, `urls.py`).
- `hms/`: Main application directory.
    - `models.py`: Database schema definitions.
    - `views.py`: Application logic and request handling.
    - `urls.py`: URL routing specific to the HMS app.
    - `forms.py`: Django forms for input validation.
    - `templates/`: HTML templates (organized by student/admin sections).
    - `static/`: CSS (Tailwind config), Images, and JS files.

## 7. Configuration Details
- **Static Files:** Configured with `WhiteNoise` for production serving.
- **Email:** Configured for SMTP (Gmail) in production, Console backend in debug mode.
- **Timezone:** Defaults to `Africa/Nairobi`.
