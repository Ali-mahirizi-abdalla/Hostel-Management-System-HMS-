"""
Notification Utilities for HMS
Supports Email and SMS notifications
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Unified notification service for email and SMS"""
    
    @staticmethod
    def send_email(to_email, subject, message, html_message=None):
        """Send email notification
        
        Args:
            to_email: Recipient email address (str or list)
            subject: Email subject
            message: Plain text message
            html_message: Optional HTML message
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            if isinstance(to_email, str):
                to_email = [to_email]
            
            if html_message:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=to_email
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)
            else:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=to_email,
                    fail_silently=False
                )
            
            logger.info(f"Email sent to {to_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_sms(phone_number, message):
        """Send SMS notification
        
        This is a placeholder that can be integrated with:
        - Twilio
        - Africa's Talking
        - Any other SMS gateway
        
        Args:
            phone_number: Recipient phone number
            message: SMS message (keep under 160 chars for single SMS)
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Check if SMS is configured
            if not getattr(settings, 'SMS_ENABLED', False):
                logger.warning("SMS is not enabled. Configure SMS_ENABLED in settings.")
                return False
            
            # Example: Twilio integration
            if getattr(settings, 'TWILIO_ACCOUNT_SID', None):
                from twilio.rest import Client
                client = Client(
                    settings.TWILIO_ACCOUNT_SID,
                    settings.TWILIO_AUTH_TOKEN
                )
                client.messages.create(
                    body=message,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=phone_number
                )
                logger.info(f"SMS sent to {phone_number}")
                return True
            
            # Example: Africa's Talking integration
            elif getattr(settings, 'AFRICASTALKING_USERNAME', None):
                import africastalking
                africastalking.initialize(
                    settings.AFRICASTALKING_USERNAME,
                    settings.AFRICASTALKING_API_KEY
                )
                sms = africastalking.SMS
                sms.send(message, [phone_number])
                logger.info(f"SMS sent to {phone_number}")
                return True
            
            else:
                logger.warning("No SMS provider configured.")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send SMS to {phone_number}: {str(e)}")
            return False


# ==================== NOTIFICATION TEMPLATES ====================

def notify_leave_request_submitted(leave_request):
    """Notify admin when a new leave request is submitted"""
    from .models import LeaveRequest
    
    admin_email = getattr(settings, 'ADMIN_EMAIL', None)
    if not admin_email:
        return False
    
    subject = f"🏠 New Leave Request from {leave_request.student.user.get_full_name()}"
    message = f"""
A new leave request has been submitted:

Student: {leave_request.student.user.get_full_name()}
University ID: {leave_request.student.university_id}
Leave Type: {leave_request.get_leave_type_display()}
Duration: {leave_request.start_date} to {leave_request.end_date}
Destination: {leave_request.destination}
Reason: {leave_request.reason}

Please review this request in the admin dashboard.
    """
    
    return NotificationService.send_email(admin_email, subject, message)


def notify_leave_request_status(leave_request):
    """Notify student when their leave request is approved/rejected"""
    student_email = leave_request.student.user.email
    student_phone = leave_request.student.phone
    
    if leave_request.status == 'approved':
        subject = "✅ Leave Request Approved"
        message = f"""
Dear {leave_request.student.user.first_name},

Your leave request has been APPROVED!

Details:
- Leave Type: {leave_request.get_leave_type_display()}
- Duration: {leave_request.start_date} to {leave_request.end_date}
- Destination: {leave_request.destination}

Admin Notes: {leave_request.admin_notes or 'None'}

Have a safe trip!

Best regards,
Hostel Management System
        """
        sms_message = f"HMS: Your leave from {leave_request.start_date} to {leave_request.end_date} is APPROVED. Have a safe trip!"
    else:
        subject = "❌ Leave Request Rejected"
        message = f"""
Dear {leave_request.student.user.first_name},

Unfortunately, your leave request has been rejected.

Details:
- Leave Type: {leave_request.get_leave_type_display()}
- Requested: {leave_request.start_date} to {leave_request.end_date}

Admin Notes: {leave_request.admin_notes or 'No reason provided'}

Please contact the hostel administration if you have questions.

Best regards,
Hostel Management System
        """
        sms_message = f"HMS: Your leave request has been REJECTED. Check your email for details."
    
    # Send email
    email_sent = NotificationService.send_email(student_email, subject, message)
    
    # Send SMS if phone available
    sms_sent = False
    if student_phone:
        sms_sent = NotificationService.send_sms(student_phone, sms_message)
    
    return email_sent or sms_sent


def notify_maintenance_status_update(maintenance_request):
    """Notify student when their maintenance request status changes"""
    student_email = maintenance_request.student.user.email
    student_phone = maintenance_request.student.phone
    
    status_emoji = {
        'pending': '🟡',
        'in_progress': '🔵',
        'resolved': '🟢'
    }
    
    emoji = status_emoji.get(maintenance_request.status, '📢')
    
    subject = f"{emoji} Maintenance Request Update: {maintenance_request.title}"
    message = f"""
Dear {maintenance_request.student.user.first_name},

Your maintenance request has been updated:

Title: {maintenance_request.title}
New Status: {maintenance_request.get_status_display()}
Priority: {maintenance_request.get_priority_display()}

Description: {maintenance_request.description}

Thank you for your patience.

Best regards,
Hostel Management System
    """
    
    sms_message = f"HMS: Your maintenance request '{maintenance_request.title}' is now {maintenance_request.get_status_display()}."
    
    # Send email
    email_sent = NotificationService.send_email(student_email, subject, message)
    
    # Send SMS if phone available
    sms_sent = False
    if student_phone:
        sms_sent = NotificationService.send_sms(student_phone, sms_message)
    
    return email_sent or sms_sent


def notify_new_announcement(announcement):
    """Notify all students about a new announcement"""
    from .models import Student
    
    students = Student.objects.select_related('user').all()
    
    priority_emoji = {
        'low': 'ℹ️',
        'normal': '📢',
        'high': '⚠️',
        'urgent': '🚨'
    }
    
    emoji = priority_emoji.get(announcement.priority, '📢')
    
    subject = f"{emoji} {announcement.title}"
    message = f"""
Dear Student,

{announcement.content}

---
This is an official announcement from the Hostel Management System.
Priority: {announcement.get_priority_display()}
Posted: {announcement.created_at.strftime('%B %d, %Y at %H:%M')}
    """
    
    # Only send SMS for high/urgent announcements
    send_sms_notification = announcement.priority in ['high', 'urgent']
    sms_message = f"HMS ({announcement.get_priority_display()}): {announcement.title[:100]}"
    
    success_count = 0
    for student in students:
        if student.user.email:
            if NotificationService.send_email(student.user.email, subject, message):
                success_count += 1
        
        if send_sms_notification and student.phone:
            NotificationService.send_sms(student.phone, sms_message)
    
    return success_count


def notify_meal_reminder(student, meal_date):
    """Send meal confirmation reminder to a student"""
    subject = f"🍽️ Reminder: Confirm Your Meals for {meal_date.strftime('%B %d')}"
    message = f"""
Dear {student.user.first_name},

This is a friendly reminder to confirm your meal preferences for {meal_date.strftime('%A, %B %d, %Y')}.

Please log in to the Hostel Management System and confirm your meals before 8:00 AM.

Best regards,
Hostel Management System
    """
    
    sms_message = f"HMS: Please confirm your meals for {meal_date.strftime('%b %d')} before 8 AM."
    
    email_sent = NotificationService.send_email(student.user.email, subject, message)
    
    if student.phone:
        NotificationService.send_sms(student.phone, sms_message)
    
    return email_sent


def send_bulk_meal_reminders():
    """Send reminders to all students who haven't confirmed meals for tomorrow"""
    from .models import Student, Meal
    from datetime import date, timedelta
    
    tomorrow = date.today() + timedelta(days=1)
    
    # Get students who haven't confirmed meals
    confirmed_ids = Meal.objects.filter(date=tomorrow).values_list('student_id', flat=True)
    unconfirmed_students = Student.objects.exclude(id__in=confirmed_ids)
    
    success_count = 0
    for student in unconfirmed_students:
        if notify_meal_reminder(student, tomorrow):
            success_count += 1
    
    return success_count, unconfirmed_students.count()
