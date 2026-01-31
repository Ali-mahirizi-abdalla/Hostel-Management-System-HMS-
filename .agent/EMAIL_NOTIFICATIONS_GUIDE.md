# 📧 Email Notification System - Setup Guide

## Overview
The Hostel Management System now includes an automated email notification system that alerts the admin about students who haven't confirmed their meals for the next day.

---

## ✅ Features Implemented

### 1. **On-Demand Email Notifications**
- **Location**: Admin Dashboard → Quick Actions Panel
- **Button**: "📧 Send Email Notifications"
- **Function**: Sends immediate email to admin about unconfirmed students

### 2. **Management Command for Automation**
- **Command**: `python manage.py send_meal_reminders`
- **Purpose**: Can be scheduled to run automatically (e.g., via cron job or Task Scheduler)

### 3. **Email Content**
The notification email includes:
- Date for which meals are unconfirmed
- Total number of unconfirmed students
- Complete list of unconfirmed students with:
  - Full name
  - University ID
  - Email address
- Direct link to admin dashboard

---

## 🔧 Configuration

### Email Settings (in `settings.py`)

```python
# Admin email for notifications
ADMIN_EMAIL = 'alimahrez744@gmail.com'
DEFAULT_FROM_EMAIL = 'Hostel Management System <noreply@hostel.com>'

# Development Mode (prints to console)
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production Mode (sends real emails via Gmail)
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'alimahrez744@gmail.com'
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
```

---

## 🚀 How to Use

### **Option 1: Manual Trigger (From Dashboard)**

1. Login as admin
2. Navigate to Kitchen Dashboard
3. Scroll to "Quick Actions" panel
4. Click "📧 Send Email Notifications"
5. Confirm the action
6. Email will be sent immediately

### **Option 2: Command Line**

Run this command manually:
```bash
python manage.py send_meal_reminders
```

### **Option 3: Automated Schedule (Recommended)**

#### **For Windows (Task Scheduler)**

1. Open Task Scheduler
2. Create a new task:
   - **Name**: "HMS Meal Reminders"
   - **Trigger**: Daily at 6:00 PM
   - **Action**: Start a program
   - **Program**: `python`
   - **Arguments**: `manage.py send_meal_reminders`
   - **Start in**: `C:\Users\jamal\OneDrive\Desktop\Hostel_System`

#### **For Linux/Mac (Cron Job)**

Add to crontab:
```bash
# Run every day at 6:00 PM
0 18 * * * cd /path/to/Hostel_System && python manage.py send_meal_reminders
```

---

## 📧 Setting Up Gmail for Production

### **Step 1: Enable 2-Factor Authentication**
1. Go to Google Account settings
2. Navigate to Security
3. Enable 2-Step Verification

### **Step 2: Generate App Password**
1. Go to Google Account → Security
2. Select "2-Step Verification"
3. Scroll to "App passwords"
4. Generate a new app password for "Mail"
5. Copy the 16-character password

### **Step 3: Set Environment Variable**

**Windows (PowerShell):**
```powershell
$env:EMAIL_HOST_PASSWORD="your-16-char-app-password"
```

**Linux/Mac:**
```bash
export EMAIL_HOST_PASSWORD="your-16-char-app-password"
```

**Or create a `.env` file:**
```
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

### **Step 4: Update `settings.py` to Use .env**

Install python-decouple:
```bash
pip install python-decouple
```

Update settings.py:
```python
from decouple import config

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
```

---

## 📊 Email Sample

```
Subject: ⚠️ Meal Confirmation Alert - 5 Students Unconfirmed for December 11, 2025

Hello Admin,

This is an automated notification from the Hostel Management System.

📅 Date: Wednesday, December 11, 2025
⚠️ Unconfirmed Students: 5 out of 50

The following students have NOT confirmed their meals for tomorrow:

  • John Doe (STU001) - john@example.com
  • Jane Smith (STU002) - jane@example.com
  • Bob Johnson (STU003) - bob@example.com
  • Alice Brown (STU004) - alice@example.com
  • Charlie Wilson (STU005) - charlie@example.com

Please remind these students to confirm their meal preferences before the deadline.

---
🔗 Access the admin dashboard: http://127.0.0.1:8000/kitchen/dashboard/

This is an automated message from Hostel Management System.
Do not reply to this email.
```

---

## 🧪 Testing

### **Test in Development (Console Output)**

1. Ensure `DEBUG = True` in settings.py
2. Click "Send Email Notifications" or run command
3. Check terminal/console for email output
4. Email content will be printed instead of sent

### **Test in Production (Real Email)**

1. Set `DEBUG = False` in settings.py
2. Configure Gmail app password
3. Run the notification
4. Check your inbox at alimahrez744@gmail.com

---

## 🔍 Troubleshooting

### **Issue: Email not sending**

**Check:**
1. ✅ Gmail app password is correct
2. ✅ Environment variable is set
3. ✅ Internet connection is active
4. ✅ Gmail account has 2FA enabled
5. ✅ Less secure app access is disabled (use app password instead)

### **Issue: "SMTPAuthenticationError"**

**Solution:**
- Verify app password is correct
- Regenerate app password if needed
- Check if 2FA is enabled on Gmail

### **Issue: No unconfirmed students message**

**This is normal!** It means all students have confirmed their meals.

---

## 📁 Files Modified

1. **`Hostel_System/settings.py`** - Email configuration
2. **`hms/views.py`** - Added `send_meal_notifications` view
3. **`hms/urls.py`** - Added URL pattern for notifications
4. **`hms/management/commands/send_meal_reminders.py`** - Management command
5. **`hms/templates/hms/admin/dashboard.html`** - Added notification button

---

## 🎯 Best Practices

### **Recommended Schedule**
- **6:00 PM Daily**: Send reminder for next day's meals
- **8:00 AM Daily**: Final reminder before breakfast deadline

### **Email Frequency**
- Don't send more than 2 emails per day
- Only send if there are unconfirmed students
- Consider adding a "last sent" timestamp to avoid duplicates

### **Future Enhancements**
1. ✅ Send emails directly to unconfirmed students
2. ✅ SMS notifications integration
3. ✅ WhatsApp notifications
4. ✅ Customizable email templates
5. ✅ Email scheduling from dashboard
6. ✅ Email logs and history

---

## 🔐 Security Notes

### **Important:**
- ⚠️ Never commit app passwords to Git
- ⚠️ Use environment variables for sensitive data
- ⚠️ Keep `.env` file in `.gitignore`
- ⚠️ Rotate app passwords periodically

### **`.gitignore` Entry:**
```
.env
*.env
.env.local
```

---

## 📞 Support

### **Common Questions**

**Q: Can I change the admin email?**
A: Yes, update `ADMIN_EMAIL` in `settings.py`

**Q: Can I send to multiple admins?**
A: Yes, change `recipient_list=[settings.ADMIN_EMAIL]` to `recipient_list=['email1@example.com', 'email2@example.com']`

**Q: How do I customize the email template?**
A: Edit the `message` variable in `send_meal_notifications` function in `views.py`

**Q: Can I use a different email provider?**
A: Yes, update `EMAIL_HOST`, `EMAIL_PORT`, and credentials in `settings.py`

---

## ✅ Quick Start Checklist

- [ ] Gmail 2FA enabled
- [ ] App password generated
- [ ] Environment variable set
- [ ] Test email sent successfully
- [ ] Automated schedule configured (optional)
- [ ] Documentation reviewed

---

## 🎉 Summary

Your Hostel Management System now has:
- ✅ Automated email notifications
- ✅ On-demand notification trigger
- ✅ Management command for scheduling
- ✅ Professional email formatting
- ✅ Secure Gmail integration
- ✅ Development and production modes

**The notification system is ready to use!** 📧
