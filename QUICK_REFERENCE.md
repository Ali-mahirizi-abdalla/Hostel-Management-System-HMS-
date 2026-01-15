# Quick Reference - Hostel Management System
## Developer: Ali Mahirizi Abdalla

---

## 🚀 Quick Start Commands

### Development Server
```bash
python manage.py runserver
```
Access at: http://127.0.0.1:8000/

### Create Superuser
```bash
python manage.py createsuperuser
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

---

## 📁 Important URLs

| Page | URL |
|------|-----|
| Home/Login | `/` |
| Student Dashboard | `/student/dashboard/` |
| Admin Dashboard | `/admin/dashboard/` |
| Django Admin | `/admin/` |
| Payment History | `/student/payments/` |
| M-Pesa Callback | `/payment/callback/` |

---

## 🔑 Default Admin Credentials

**Note:** Create your own superuser using the command above.

---

## 🎨 Customization Locations

Your name appears in:
- ✅ Footer (all pages)
- ✅ Sidebar (authenticated pages)
- ✅ Login page
- ✅ Admin dashboard
- ✅ Documentation files
- ✅ README.md
- ✅ LICENSE file

---

## 📧 Email Configuration

Current admin email: `alimahrez744@gmail.com`

To change, update in `Hostel_System/settings.py`:
```python
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'your-email@example.com')
```

---

## 💳 M-Pesa Configuration

Current settings (Sandbox):
- Consumer Key: Set in settings.py
- Consumer Secret: Set in settings.py
- Shortcode: 174379 (Sandbox)
- Callback URL: Set via ngrok

To update for production, modify `Hostel_System/settings.py`

---

## 🗄️ Database

**Development:** SQLite (`db.sqlite3`)
**Production:** PostgreSQL (via DATABASE_URL env variable)

---

## 🎯 Key Features

### For Students:
- Meal booking (breakfast, early breakfast, supper)
- Away mode for automatic meal cancellation
- Room selection and management
- Maintenance request submission
- Leave request application
- M-Pesa payment for accommodation fees
- Direct chat with admin

### For Admins:
- Student management
- Meal tracking and CSV export
- Leave request approval
- Maintenance ticket management
- Payment tracking
- Analytics dashboard
- Announcement posting
- Event management

---

## 🔧 Troubleshooting

### Static files not loading?
```bash
python manage.py collectstatic --noinput
```

### Database issues?
```bash
python manage.py migrate --run-syncdb
```

### M-Pesa not working?
1. Check ngrok is running
2. Verify callback URL in settings
3. Check M-Pesa credentials

---

## 📱 Responsive Design

The system is fully responsive and works on:
- ✅ Desktop (1920px+)
- ✅ Laptop (1366px+)
- ✅ Tablet (768px+)
- ✅ Mobile (320px+)

---

## 🌙 Dark Mode

Dark mode is available and toggles automatically based on:
- User preference (saved in localStorage)
- System preference (if no saved preference)

Toggle button is in the top navigation bar.

---

## 📊 Analytics

Admin dashboard includes:
- Daily meal counts
- Weekly trends chart
- Room occupancy rates
- Away student tracking
- Payment statistics

---

## 🔐 Security Features

- ✅ CSRF protection
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection
- ✅ Secure password hashing
- ✅ HTTPS redirect (production)
- ✅ Session security

---

## 📝 Important Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management script |
| `requirements.txt` | Python dependencies |
| `db.sqlite3` | Development database |
| `settings.py` | Django configuration |
| `urls.py` | URL routing |
| `views.py` | Application logic |
| `models.py` | Database models |
| `mpesa.py` | M-Pesa integration |

---

## 🎓 Models Overview

- **Student** - Extended user profile
- **Room** - Room information
- **RoomAssignment** - Student-room mapping
- **Meal** - Daily meal records
- **AwayPeriod** - Away date ranges
- **MaintenanceRequest** - Maintenance tickets
- **LeaveRequest** - Leave applications
- **Payment** - M-Pesa transactions
- **Announcement** - System announcements
- **Activity** - Weekly activities
- **Event** - Hostel events
- **Visitor** - Visitor logs

---

## 🚀 Deployment Checklist

- [ ] Set DEBUG=False
- [ ] Configure DATABASE_URL
- [ ] Set SECRET_KEY (environment variable)
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up CSRF_TRUSTED_ORIGINS
- [ ] Configure email settings
- [ ] Set up M-Pesa production credentials
- [ ] Run collectstatic
- [ ] Run migrations
- [ ] Create superuser

---

## 📞 Support

**Developer:** Ali Mahirizi Abdalla  
**Email:** alimahrez744@gmail.com  
**Project:** Hostel Management System v2.0  

---

**© 2026 Ali Mahirizi Abdalla. All rights reserved.**

Built with ❤️ using Django, Tailwind CSS, and M-Pesa API
