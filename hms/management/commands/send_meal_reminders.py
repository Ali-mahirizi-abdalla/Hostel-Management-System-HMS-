from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, timedelta
from hms.models import Student, Meal


class Command(BaseCommand):
    help = 'Send email notifications to admin about unconfirmed students for tomorrow'

    def handle(self, *args, **options):
        tomorrow = date.today() + timedelta(days=1)
        
        # Get all students
        all_students = Student.objects.all()
        
        # Get students who have confirmed meals for tomorrow
        confirmed_student_ids = Meal.objects.filter(
            date=tomorrow
        ).values_list('student_id', flat=True)
        
        # Find unconfirmed students
        unconfirmed_students = all_students.exclude(id__in=confirmed_student_ids)
        
        if not unconfirmed_students.exists():
            self.stdout.write(
                self.style.SUCCESS('✅ All students have confirmed their meals for tomorrow!')
            )
            return
        
        # Prepare email content
        unconfirmed_count = unconfirmed_students.count()
        student_list = '\n'.join([
            f"  • {student.user.get_full_name()} ({student.university_id}) - {student.user.email}"
            for student in unconfirmed_students
        ])
        
        subject = f'⚠️ Meal Confirmation Alert - {unconfirmed_count} Students Unconfirmed for {tomorrow.strftime("%B %d, %Y")}'
        
        message = f"""
Hello Admin,

This is an automated notification from the Hostel Management System.

📅 Date: {tomorrow.strftime("%A, %B %d, %Y")}
⚠️ Unconfirmed Students: {unconfirmed_count} out of {all_students.count()}

The following students have NOT confirmed their meals for tomorrow:

{student_list}

Please remind these students to confirm their meal preferences before the deadline.

---
🔗 Access the admin dashboard: http://127.0.0.1:8000/kitchen/dashboard/

This is an automated message from Hostel Management System.
Do not reply to this email.
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Email sent successfully to {settings.ADMIN_EMAIL}\n'
                    f'   {unconfirmed_count} unconfirmed students for {tomorrow}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send email: {str(e)}')
            )
