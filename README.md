# Hostel Management System (HMS)

![HMS Banner](https://img.shields.io/badge/HMS-Hostel%20Management%20System-blue)
![Version](https://img.shields.io/badge/version-2.0-green)
![Django](https://img.shields.io/badge/Django-4.2-success)
![License](https://img.shields.io/badge/license-MIT-orange)

## 👨‍💻 Developer Information

**Name:** Ali Mahirizi Abdalla  
**Project:** Hostel Management System  
**Version:** 2.0  
**Technology Stack:** Django, Python, Tailwind CSS, SQLite/PostgreSQL  

---

## 📋 Overview

The **Hostel Management System (HMS)** is a comprehensive web-based application designed to streamline and digitize hostel operations. Built with Django and modern web technologies, it provides an intuitive interface for both students and administrators to manage accommodation, meals, maintenance requests, and communication efficiently.

## ✨ Key Features

### For Students
- **📊 Dashboard:** Centralized hub with announcements, meal status, and quick actions
- **👤 Profile Management:** Update personal information, upload profile pictures and timetables
- **🏠 Room Management:** View available rooms, select specific beds, request room changes
- **🍽️ Meal Management:** Book meals (Breakfast, Early Breakfast, Supper) for today and tomorrow
- **✈️ Away Mode:** Mark yourself as away to automatically opt-out of meals
- **🔧 Maintenance Requests:** Report issues with photos and track repair status
- **📝 Leave Requests:** Apply for leave and track approval status
- **💬 Communication:** Direct chat interface with hostel administration
- **💳 M-Pesa Integration:** Pay accommodation fees via M-Pesa STK Push

### For Administrators
- **📈 Analytics Dashboard:** View meal consumption, room occupancy, and system health
- **👥 Student Management:** Add, edit, or remove student profiles
- **🏢 Room Management:** Create rooms, manage assignments, handle change requests
- **🍳 Kitchen Management:** View daily meal counts, export data to CSV
- **✅ Request Oversight:** Approve/reject leave requests and maintenance tickets
- **👁️ Visitor Management:** Log and track visitors
- **📢 Announcements:** Post system-wide updates for students
- **💰 Payment Management:** Track M-Pesa payments and accommodation fees

## 🛠️ Technology Stack

- **Backend:** Django 4.2 (Python)
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **Authentication:** Django Auth + django-allauth (Google OAuth)
- **Payment:** M-Pesa Daraja API (STK Push)
- **Deployment:** Render, Vercel compatible
- **Static Files:** WhiteNoise

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Hostel-Management-System-HMS-
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   - Open your browser and navigate to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## 📁 Project Structure

```
Hostel-Management-System-HMS-/
├── Hostel_System/          # Main project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── hms/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URL routing
│   ├── forms.py           # Django forms
│   ├── mpesa.py           # M-Pesa integration
│   ├── templates/         # HTML templates
│   │   ├── hms/
│   │   │   ├── student/   # Student templates
│   │   │   ├── admin/     # Admin templates
│   │   │   └── kitchen/   # Kitchen templates
│   └── static/            # CSS, JS, Images
├── media/                 # User uploaded files
├── staticfiles/           # Collected static files
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
└── README.md             # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ADMIN_EMAIL=your-email@example.com

# M-Pesa Configuration
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_SHORTCODE=your-shortcode
MPESA_PASSKEY=your-passkey
MPESA_CALLBACK_URL=your-callback-url

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Email Configuration (Production)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🗄️ Database Models

- **Student:** Extended user model with university ID, phone, profile picture
- **Room:** Room details (number, capacity, type, availability)
- **RoomAssignment:** Links students to rooms
- **Meal:** Daily meal choices per student
- **AwayPeriod:** Tracks when students are away
- **MaintenanceRequest:** Maintenance tickets with priority and status
- **LeaveRequest:** Leave applications with approval workflow
- **Visitor:** Visitor logs with time in/out
- **Payment:** M-Pesa payment records
- **Announcement:** System-wide announcements
- **Activity:** Weekly scheduled activities

## 🌐 Deployment

### Render Deployment

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Set environment variables
5. Deploy!

The project includes:
- `build.sh` - Build script for Render
- `render.yaml` - Render configuration
- `Procfile` - Process file for deployment

### Vercel Deployment

The project includes `vercel.json` for Vercel deployment.

## 📱 M-Pesa Integration

The system integrates with Safaricom's M-Pesa Daraja API for accommodation fee payments:

- **STK Push:** Initiates payment prompts on student phones
- **Callback Handling:** Processes payment confirmations
- **Payment History:** Students can view their payment records
- **Admin Dashboard:** Track all payments and pending transactions

## 🎨 Features Highlights

- **Dark Mode:** Full dark mode support with theme toggle
- **Responsive Design:** Works seamlessly on desktop, tablet, and mobile
- **Real-time Updates:** Live meal booking status
- **File Uploads:** Support for profile pictures, timetables, and maintenance photos
- **CSV Export:** Export meal data for kitchen staff
- **Email Notifications:** Automated notifications for important events
- **Analytics:** Comprehensive analytics dashboard for administrators

## 📝 License

This project is licensed under the MIT License.

## 👤 Contact

**Ali Mahirizi Abdalla**  
Developer & Maintainer

---

## 🙏 Acknowledgments

- Built with Django and Tailwind CSS
- M-Pesa integration powered by Safaricom Daraja API
- Icons from Heroicons
- Fonts from Google Fonts

---

**© 2026 Ali Mahirizi Abdalla. All rights reserved.**
