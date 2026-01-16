from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import (Student, Meal, Activity, AwayPeriod, Announcement, Document, Message, MaintenanceRequest,
                     Room, RoomAssignment, RoomChangeRequest, LeaveRequest, Visitor, Event, EventRSVP, Payment, Notification)
from .forms import (
    StudentRegistrationForm, AwayModeForm, ActivityForm, DocumentForm, 
    TimetableForm, RoomSelectionForm, MessageForm, MaintenanceRequestForm,
    MaintenanceStatusForm, RoomForm, RoomAssignmentForm, RoomChangeRequestForm,
    LeaveRequestForm, LeaveApprovalForm, VisitorForm, EventForm, EventRSVPForm
)
from datetime import date, datetime, time, timedelta
from django.db import transaction, models
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from .mpesa import MpesaClient

# ==================== Authentication ====================

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    student = form.save()
                
                # Log in AFTER transaction commits to avoid session race conditions
                login(request, student.user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Registration successful!')
                return redirect('hms:student_dashboard')

            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
    else:
        form = StudentRegistrationForm()
    return render(request, 'hms/registration/register.html', {'form': form})


def user_login(request):
    """Login view for all users"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('hms:admin_dashboard')
        return redirect('hms:student_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            
            # Redirect based on role
            if user.is_staff:
                 return redirect('hms:admin_dashboard') 
            return redirect('hms:student_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'hms/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('hms:login')

# ==================== Student ====================

@login_required
def student_dashboard(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        if request.user.is_staff:
            return redirect('hms:admin_dashboard')
        # Auto-create profile
        student = Student.objects.create(user=request.user, university_id=None)
        messages.warning(request, "Profile was missing and has been created.")
        
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # Check if currently away
    is_away_today = AwayPeriod.objects.filter(student=student, start_date__lte=today, end_date__gte=today).exists()
    is_away_tomorrow = AwayPeriod.objects.filter(student=student, start_date__lte=tomorrow, end_date__gte=tomorrow).exists()

    # Get meal status for today and tomorrow
    meal_today, _ = Meal.objects.get_or_create(student=student, date=today)
    if is_away_today and not meal_today.away:
         # Auto-correct to away if valid period exists
         meal_today.away = True
         meal_today.breakfast = False
         meal_today.early = False
         meal_today.supper = False
         meal_today.save()

    meal_tomorrow, _ = Meal.objects.get_or_create(student=student, date=tomorrow)
    if is_away_tomorrow and not meal_tomorrow.away:
         meal_tomorrow.away = True
         meal_tomorrow.breakfast = False
         meal_tomorrow.early = False
         meal_tomorrow.supper = False
         meal_tomorrow.save()
    
    # Check lock time for UI display
    now = timezone.now()
    lock_time = time(8, 0)
    is_locked = (now.time() > lock_time)

    # Away Mode Form
    away_form = AwayModeForm()

    context = {
        'student': student,
        'meal_today': meal_today,
        'meal_tomorrow': meal_tomorrow,
        'is_locked': is_locked,
        'today': today,
        'tomorrow': tomorrow,
        'is_away_today': is_away_today,
        'is_away_tomorrow': is_away_tomorrow,
        'away_form': away_form,
        # Pre-calculated attributes for template to avoid formatter breaking split tags
        'today_breakfast_attr': 'checked' if meal_today.breakfast else '',
        'today_early_attr': 'checked' if meal_today.early else '',
        'today_supper_attr': 'checked' if meal_today.supper else '',
        'today_disabled_attr': 'disabled' if (is_locked or is_away_today) else '',
        'tomorrow_breakfast_attr': 'checked' if meal_tomorrow.breakfast else '',
        'tomorrow_early_attr': 'checked' if meal_tomorrow.early else '',
        'tomorrow_supper_attr': 'checked' if meal_tomorrow.supper else '',
        'tomorrow_disabled_attr': 'disabled' if is_away_tomorrow else '',
        'announcements': Announcement.objects.filter(is_active=True).order_by('-created_at')[:5],
        'activities': Activity.objects.filter(active=True).order_by('weekday', 'time'),
        'documents': Document.objects.all().order_by('-uploaded_at'),
        'unread_messages': Message.objects.filter(recipient=request.user, is_read=False).count(),
    }
    return render(request, 'hms/student/dashboard.html', context)

@login_required
def student_profile(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        student = Student.objects.create(user=request.user, university_id=None)
        messages.warning(request, "Profile was missing and has been created.")

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            phone = request.POST.get('phone')
            if phone:
                student.phone = phone
            
            if 'profile_image' in request.FILES:
                student.profile_image = request.FILES['profile_image']
            
            student.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('hms:student_profile')

    # Get recent meal history
    meal_history = student.meals.all().order_by('-date')[:10]
    
    # Forms
    room_form = RoomSelectionForm(instance=student)
    timetable_form = TimetableForm(instance=student)

    context = {
        'student': student,
        'meal_history': meal_history,
        'room_form': room_form,
        'timetable_form': timetable_form
    }
    return render(request, 'hms/student/profile.html', context)


@login_required
def confirm_meals(request):
    """Handle meal confirmation"""
    if request.method != 'POST':
        return HttpResponseForbidden("Method not allowed")
    
    try:
        student = request.user.student_profile
        meal_date_str = request.POST.get('date')
        meal_date = datetime.strptime(meal_date_str, '%Y-%m-%d').date()

        # Check away status first
        if AwayPeriod.objects.filter(student=student, start_date__lte=meal_date, end_date__gte=meal_date).exists():
            messages.error(request, "You are marked as away for this date. Change your 'Away Mode' settings first.")
            return redirect('hms:student_dashboard')
        
        # Enforce 8:00 AM Lock for breakfast/early
        now = timezone.now()
        current_time = now.time()
        lock_time = time(8, 0)
        is_today = (meal_date == date.today())
        
        breakfast = request.POST.get('breakfast') == 'on'
        early = request.POST.get('early') == 'on'
        supper = request.POST.get('supper') == 'on'
        
        if is_today and current_time > lock_time:
            # Cannot change breakfast/early settings after lock time
            existing, _ = Meal.objects.get_or_create(student=student, date=meal_date)
            breakfast = existing.breakfast
            early = existing.early 
            messages.warning(request, "Breakfast options are locked for today after 08:00 AM.")
            
        Meal.objects.update_or_create(
            student=student,
            date=meal_date,
            defaults={
                'breakfast': breakfast,
                'early': early,
                'supper': supper,
                'away': False
            }
        )
        messages.success(request, f"Meals updated for {meal_date}")
        
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        
    return redirect('hms:student_dashboard')

@login_required
def toggle_away_mode(request):
    if request.method == 'POST':
        form = AwayModeForm(request.POST)
        if form.is_valid():
            try:
                student = request.user.student_profile
                away_period = form.save(commit=False)
                away_period.student = student
                away_period.save()
                
                # Auto-update meals in this range to Away=True, Others=False
                cur_date = away_period.start_date
                while cur_date <= away_period.end_date:
                    Meal.objects.update_or_create(
                        student=student,
                        date=cur_date,
                        defaults={'away': True, 'breakfast': False, 'early': False, 'supper': False}
                    )
                    cur_date += timedelta(days=1)
                    
                messages.success(request, f"Away mode set from {away_period.start_date} to {away_period.end_date}")
            except Exception as e:
                 messages.error(request, f"Error setting away mode: {str(e)}")
        else:
            messages.error(request, "Invalid dates provided.")
    return redirect('hms:student_dashboard')

@login_required
def toggle_early_breakfast(request):
    return redirect('hms:student_dashboard')

# ==================== Admin/Kitchen ====================

@login_required
def dashboard_admin(request):
    """Kitchen/Admin Dashboard"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # Counts for Today
    today_stats = {
        'breakfast': Meal.objects.filter(date=today, breakfast=True).count(),
        'early': Meal.objects.filter(date=today, early=True).count(),
        'supper': Meal.objects.filter(date=today, supper=True).count(),
        'away': Meal.objects.filter(date=today, away=True).count(),
    }
    
    # Counts for Tomorrow
    tomorrow_stats = {
        'breakfast': Meal.objects.filter(date=tomorrow, breakfast=True).count(),
        'early': Meal.objects.filter(date=tomorrow, early=True).count(),
        'supper': Meal.objects.filter(date=tomorrow, supper=True).count(),
    }
    
    total_students = Student.objects.count()
    
    # Activities
    activities = Activity.objects.filter(active=True)
    today_activity = activities.filter(weekday=today.weekday()).first()
    
    context = {
        'today': today,
        'tomorrow': tomorrow,
        'today_stats': today_stats,
        'tomorrow_stats': tomorrow_stats,
        'total_students': total_students,
        'today_activity': today_activity,
        'activities': activities
    }

    # ==================== ADVANCED DASHBOARD LOGIC ====================
    
    # 1. Search & Filtering
    search_query = request.GET.get('q', '')
    filter_date_str = request.GET.get('date', str(today))
    
    try:
        filter_date = datetime.strptime(filter_date_str, '%Y-%m-%d').date()
    except ValueError:
        filter_date = today

    # Base Queryset for Today's Meals (or filtered date)
    meals_query = Meal.objects.filter(date=filter_date).select_related('student__user')
    
    if search_query:
        meals_query = meals_query.filter(
            models.Q(student__user__first_name__icontains=search_query) | 
            models.Q(student__user__last_name__icontains=search_query) |
            models.Q(student__university_id__icontains=search_query)
        )

    # 2. Daily Lists
    present_list = meals_query.filter(away=False)
    
    # Filter by meal type if requested
    filter_type = request.GET.get('filter')
    if filter_type == 'breakfast':
        present_list = present_list.filter(breakfast=True)
    elif filter_type == 'supper':
        present_list = present_list.filter(supper=True)
    elif filter_type == 'early':
        present_list = present_list.filter(early=True)

    # Students who have explicitly set 'away' to True for this date
    away_list_consult = meals_query.filter(away=True)
    
    # 3. Notifications / "Unconfirmed" 
    # Logic: Students who have a profile but NO meal record for tomorrow
    # This might differ based on business logic, here assuming "No Record" = Unconfirmed
    all_student_ids = Student.objects.values_list('id', flat=True)
    confirmed_student_ids_tomorrow = Meal.objects.filter(date=tomorrow).values_list('student_id', flat=True)
    unconfirmed_count = len(all_student_ids) - len(confirmed_student_ids_tomorrow)

    # 4. Chart Data: Weekly Trends (Last 7 Days)
    week_start = today - timedelta(days=6)
    weekly_labels = []
    weekly_breakfast = []
    weekly_supper = []
    
    for i in range(7):
        d = week_start + timedelta(days=i)
        weekly_labels.append(d.strftime('%a')) # Mon, Tue...
        stats = Meal.objects.filter(date=d).aggregate(
            b_count=models.Count('id', filter=models.Q(breakfast=True)),
            s_count=models.Count('id', filter=models.Q(supper=True))
        )
        weekly_breakfast.append(stats['b_count'])
        weekly_supper.append(stats['s_count'])

    import json
    chart_data = {
        'weekly_labels': weekly_labels,
        'weekly_breakfast': weekly_breakfast,
        'weekly_supper': weekly_supper,
    }

    context.update({
        'filter_date': filter_date,
        'search_query': search_query,
        'filter_type': filter_type,
        'meals_list': present_list,
        'away_list_consult': away_list_consult, # Renamed to avoid confusion with AwayPeriod
        'unconfirmed_count': unconfirmed_count,
        'chart_data_json': json.dumps(chart_data),
    })

    return render(request, 'hms/admin/dashboard.html', context)

@login_required
def export_meals_csv(request):
    """Export confirmed meals to CSV"""
    if not request.user.is_staff:
        return HttpResponseForbidden("Access denied")
    
    import csv
    
    date_str = request.GET.get('date', str(date.today()))
    try:
        query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        query_date = date.today()
        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="meals_{query_date}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'University ID', 'Breakfast', 'Early', 'Supper', 'Away', 'Phone'])
    
    meals = Meal.objects.filter(date=query_date).select_related('student__user')
    
    for meal in meals:
        writer.writerow([
            meal.student.user.get_full_name(),
            meal.student.university_id,
            'Yes' if meal.breakfast else 'No',
            'Yes' if meal.early else 'No',
            'Yes' if meal.supper else 'No',
            'Yes' if meal.away else 'No',
            meal.student.phone
        ])
        
    return response

@login_required
def send_meal_notifications(request):
    """Send email notifications about unconfirmed students"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    from django.core.mail import send_mail
    from django.conf import settings
    
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
        messages.success(request, '✅ All students have confirmed their meals for tomorrow!')
        return redirect('hms:admin_dashboard')
    
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
🔗 Access the admin dashboard: {request.build_absolute_uri('/kitchen/dashboard/')}

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
        
        messages.success(
            request, 
            f'✅ Email notification sent successfully to {settings.ADMIN_EMAIL}! '
            f'{unconfirmed_count} unconfirmed students for {tomorrow.strftime("%B %d")}'
        )
        
    except Exception as e:
        messages.error(request, f'❌ Failed to send email: {str(e)}')
    
    return redirect('hms:admin_dashboard')

@login_required
def manage_students(request):
    """List and filter students (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    search_query = request.GET.get('search', '')
    students = Student.objects.all().select_related('user').order_by('user__first_name')
    
    if search_query:
        students = students.filter(
            models.Q(user__first_name__icontains=search_query) |
            models.Q(user__last_name__icontains=search_query) |
            models.Q(university_id__icontains=search_query)
        )
    
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'hms/admin/manage_students.html', context)

@login_required
def add_student(request):
    """Add a new student (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('hms:manage_students')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'hms/registration/register.html', {'form': form, 'title': 'Add New Student'})

@login_required
def edit_student(request, user_id):
    """Edit student profile (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    user = get_object_or_404(User, id=user_id)
    student = get_object_or_404(Student, user=user)
    
    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Update student fields
        student.university_id = request.POST.get('university_id', '')
        student.phone = request.POST.get('phone', '')
        student.room_number = request.POST.get('room_number', '')
        student.is_away = request.POST.get('is_away') == 'on'
        student.is_warden = request.POST.get('is_warden') == 'on'
        student.save()
        
        messages.success(request, 'Student profile updated successfully!')
        return redirect('hms:manage_students')
    
    return render(request, 'hms/admin/edit_student.html', {'student': student})

@login_required
def delete_student(request, user_id):
    """Delete student (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('hms:student_dashboard')
    
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('hms:manage_students')
        
    user = get_object_or_404(User, id=user_id)
    student_name = user.get_full_name() or user.username
    user.delete()
    messages.success(request, f"Student '{student_name}' deleted successfully.")
    return redirect('hms:manage_students')

@login_required
def student_details(request, user_id):
    """View student details (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('hms:student_dashboard')
        
    user = get_object_or_404(User, id=user_id)
    student = get_object_or_404(Student, user=user)
    meal_history = student.meals.all().order_by('-date')[:15]
    
    return render(request, 'hms/admin/student_details.html', {
        'student': student,
        'meal_history': meal_history
    })

@login_required
def away_list(request):
    """View list of students currently away (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('hms:student_dashboard')
        
    today = date.today()
    away_periods = AwayPeriod.objects.filter(start_date__lte=today, end_date__gte=today).select_related('student__user')
    
    return render(request, 'hms/admin/students.html', {'students': [ap.student for ap in away_periods]})

# ==================== Announcements ====================

@login_required
def announcements_list(request):
    """View all announcements"""
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')
    context = {
        'announcements': announcements
    }
    return render(request, 'hms/student/announcements.html', context)

@login_required
def manage_announcements(request):
    """Manage announcements (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    announcements = Announcement.objects.all().order_by('-created_at')
    
    if search_query:
        announcements = announcements.filter(
            models.Q(title__icontains=search_query) |
            models.Q(content__icontains=search_query)
        )
    
    if status_filter == 'active':
        announcements = announcements.filter(is_active=True)
    elif status_filter == 'inactive':
        announcements = announcements.filter(is_active=False)
        
    paginator = Paginator(announcements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'hms/admin/manage_announcements.html', context)

@login_required
def delete_announcement(request, pk):
    """Delete an announcement (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('hms:student_dashboard')
    
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('hms:manage_announcements')
        
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement_title = announcement.title
    announcement.delete()
    messages.success(request, f"Announcement '{announcement_title}' deleted successfully.")
    return redirect('hms:manage_announcements')

@login_required
def edit_announcement(request, pk):
    """Edit an announcement (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('hms:student_dashboard')
        
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        announcement.title = request.POST.get('title')
        announcement.content = request.POST.get('content')
        announcement.priority = request.POST.get('priority', 'normal')
        announcement.is_active = request.POST.get('is_active') == 'on'
        announcement.save()
        messages.success(request, "Announcement updated successfully.")
        return redirect('hms:manage_announcements')
        
    return render(request, 'hms/admin/announcement_form.html', {'announcement': announcement, 'edit_mode': True})


@login_required
def create_announcement(request):
    """Create new announcement"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    from .models import Announcement
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        priority = request.POST.get('priority', 'normal')
        is_active = request.POST.get('is_active') == 'on'
        
        announcement = Announcement.objects.create(
            title=title,
            content=content,
            priority=priority,
            is_active=is_active,
            created_by=request.user
        )
        
        # Send notifications only if announcement is active
        if is_active:
            try:
                from .notifications import notify_new_announcement
                notify_new_announcement(announcement)
                messages.success(request, 'Announcement created successfully and notifications sent!')
            except Exception as e:
                messages.warning(request, f'Announcement created but notifications failed: {str(e)}')
        else:
            messages.success(request, 'Announcement created successfully (inactive - no notifications sent).')
        
        return redirect('hms:manage_announcements')
    
    # GET request - show list of recent announcements
    announcements = Announcement.objects.all().order_by('-created_at')[:10]
    return render(request, 'hms/admin/announcements.html', {'announcements': announcements})

# ==================== Activities ====================

@login_required
def activities_list(request):
    """View and manage all activities"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    activities = Activity.objects.all().order_by('weekday', 'time')
    context = {
        'activities': activities
    }
    return render(request, 'hms/admin/activities.html', context)

@login_required
def create_activity(request):
    """Create a new activity"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    if request.method == 'POST':
        display_name = request.POST.get('display_name', '')
        weekday = request.POST.get('weekday', 0)
        time_str = request.POST.get('time', '')
        description = request.POST.get('description', '')
        is_active = request.POST.get('active') == 'on'
        
        activity = Activity.objects.create(
            display_name=display_name,
            weekday=int(weekday),
            time=time_str if time_str else None,
            description=description,
            active=is_active
        )
        messages.success(request, f"Activity '{display_name}' created successfully!")
        return redirect('hms:activities')
    
    return render(request, 'hms/admin/activity_form.html', {'edit_mode': False})

@login_required
def edit_activity(request, pk):
    """Edit an existing activity"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    activity = get_object_or_404(Activity, pk=pk)
    
    if request.method == 'POST':
        activity.display_name = request.POST.get('display_name', '')
        activity.weekday = int(request.POST.get('weekday', 0))
        time_str = request.POST.get('time', '')
        activity.time = time_str if time_str else None
        activity.description = request.POST.get('description', '')
        activity.active = request.POST.get('active') == 'on'
        activity.save()
        messages.success(request, f"Activity '{activity.display_name}' updated successfully!")
        return redirect('hms:activities')
    
    return render(request, 'hms/admin/activity_form.html', {'activity': activity, 'edit_mode': True})

@login_required
def delete_activity(request, pk):
    """Delete an activity"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('hms:activities')
    
    activity = get_object_or_404(Activity, pk=pk)
    activity_name = activity.display_name
    activity.delete()
    messages.success(request, f"Activity '{activity_name}' deleted successfully!")
    return redirect('hms:activities')

@login_required
def toggle_activity_status(request, pk):
    """Toggle activity active status"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('hms:activities')
    
    activity = get_object_or_404(Activity, pk=pk)
    activity.active = not activity.active
    activity.save()
    status = "activated" if activity.active else "deactivated"
    messages.success(request, f"Activity '{activity.display_name}' {status}!")
    return redirect('hms:activities')

# ==================== Additional Features ====================

@login_required
def upload_document(request):
    """Admin upload document"""
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('hms:student_dashboard')
        
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Document uploaded successfully.")
            return redirect('hms:admin_dashboard')
    else:
        form = DocumentForm()
    return render(request, 'hms/admin/upload_document.html', {'form': form})

@login_required
def upload_timetable(request):
    """Student upload timetable"""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('hms:student_dashboard')
        
    if request.method == 'POST':
        form = TimetableForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Timetable uploaded successfully.")
            return redirect('hms:student_profile')
    return redirect('hms:student_profile')

@login_required
def select_room(request):
    """Student select room"""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('hms:student_dashboard')
        
    if request.method == 'POST':
        form = RoomSelectionForm(request.POST, instance=student)
        if form.is_valid():
            room_number = form.cleaned_data['room_number']
            
            # Find the room object
            try:
                room = Room.objects.get(room_number=room_number)
                
                # Check if already assigned to this room
                if student.room_number == room_number:
                    messages.info(request, f"You are already in Room {room_number}.")
                    return redirect('hms:student_profile')

                # Check availability (double check)
                if not room.is_available:
                     messages.error(request, f"Room {room_number} is not available.")
                     return redirect('hms:student_profile')
                     
                # Create Room Assignment
                # First, end any active assignments
                RoomAssignment.objects.filter(student=student, is_active=True).update(is_active=False, checkout_date=timezone.now())
                
                # Create new assignment
                RoomAssignment.objects.create(
                    student=student,
                    room=room,
                    bed_number=1, # Defaulting to 1 for now, logic can be enhanced
                    is_active=True
                )
                
                # Update student profile for display
                student.room_number = room_number
                student.save()
                
                messages.success(request, f"Successfully assigned to Room {room_number}.")
                
            except Room.DoesNotExist:
                messages.error(request, "Selected room does not exist.")
        else:
            messages.error(request, "Invalid room selection.")
            
    return redirect('hms:student_profile')

@login_required
def chat_view(request, recipient_id=None):
    """Chat interface"""
    if request.user.is_staff:
        # Admin view: List students
        students = Student.objects.all().select_related('user')
        
        # Calculate unread counts
        for s in students:
            s.unread_count = Message.objects.filter(sender=s.user, recipient=request.user, is_read=False).count()

        if recipient_id:
             other_user = get_object_or_404(User, id=recipient_id)
        else:
             other_user = None
    else:
        # Student view: Chat with Admin 
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            messages.error(request, "No admin available to chat.")
            return redirect('hms:student_dashboard')
        other_user = admin_user
        students = None
        
    messages_qs = []
    if other_user:
        messages_qs = Message.objects.filter(
            (models.Q(sender=request.user) & models.Q(recipient=other_user)) |
            (models.Q(sender=other_user) & models.Q(recipient=request.user))
        ).order_by('timestamp')
        
        # Mark as read
        Message.objects.filter(recipient=request.user, sender=other_user).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid() and other_user:
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = other_user
            msg.save()
            # Redirect to avoid form resubmission
            if request.user.is_staff:
                 return redirect('hms:chat_with', recipient_id=other_user.id)
            else:
                 return redirect('hms:chat')
            
    else:
        form = MessageForm()
        
    context = {
        'other_user': other_user,
        'messages': messages_qs,
        'form': form,
        'students': students
    }
    return render(request, 'hms/chat.html', context)

# ==================== Maintenance Requests ====================

@login_required
def submit_maintenance_request(request):
    """View for students to submit a maintenance ticket"""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('hms:student_dashboard')

    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.student = student
            maintenance_request.save()
            messages.success(request, 'Maintenance request submitted successfully!')
            return redirect('hms:student_maintenance_list')
    else:
        form = MaintenanceRequestForm()
    
    return render(request, 'hms/student/maintenance_form.html', {'form': form})

@login_required
def student_maintenance_list(request):
    """View for students to see their maintenance tickets"""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
         return redirect('hms:student_dashboard')

    requests = MaintenanceRequest.objects.filter(student=student).order_by('-created_at')
    
    return render(request, 'hms/student/maintenance_list.html', {'requests': requests})

@login_required
def delete_maintenance_request(request, pk):
    """Student deletes their pending maintenance request"""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
         return redirect('hms:student_dashboard')

    maintenance_req = get_object_or_404(MaintenanceRequest, pk=pk, student=student)
    
    if maintenance_req.status != 'pending':
        messages.error(request, "Cannot delete request that is already in progress or resolved.")
        return redirect('hms:student_maintenance_list')
        
    if request.method == 'POST':
        maintenance_req.delete()
        messages.success(request, "Maintenance request cancelled successfully.")
    
    return redirect('hms:student_maintenance_list')

@login_required
def manage_maintenance(request):
    """Admin view to manage maintenance tickets"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
        
    requests = MaintenanceRequest.objects.all().select_related('student__user').order_by(
        models.Case(
            models.When(status='pending', then=0),
            models.When(status='in_progress', then=1),
            models.When(status='resolved', then=2),
            default=3,
        ),
        '-created_at'
    )
    
    return render(request, 'hms/admin/maintenance_list.html', {'requests': requests})

@login_required
def update_maintenance_status(request, pk):
    """Admin view to update status of a ticket"""
    if not request.user.is_staff:
         return redirect('hms:student_dashboard')
         
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(MaintenanceRequest.STATUS_CHOICES):
            maintenance_request.status = status
            maintenance_request.save()
            
            # Send notification
            from .notifications import notify_maintenance_status_update
            notify_maintenance_status_update(maintenance_request)
            
            messages.success(request, f"Status updated to {maintenance_request.get_status_display()}")
        
    return redirect('hms:manage_maintenance')


# ==================== ROOM MANAGEMENT ====================

@login_required
def room_list(request):
    """View all rooms (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    rooms = Room.objects.all().order_by('block', 'floor', 'room_number')
    
    # Filter by block if provided
    block_filter = request.GET.get('block')
    if block_filter:
        rooms = rooms.filter(block__icontains=block_filter)
    
    # Filter by availability
    availability = request.GET.get('availability')
    if availability == 'available':
        rooms = rooms.filter(is_available=True)
    elif availability == 'occupied':
        rooms = rooms.filter(is_available=False)
    
    context = {
        'rooms': rooms,
        'total_rooms': Room.objects.count(),
        'available_rooms': Room.objects.filter(is_available=True).count(),
        'occupied_rooms': Room.objects.filter(is_available=False).count(),
    }
    
    return render(request, 'hms/admin/room_list.html', context)


@login_required
def create_room(request):
    """Create a new room (admin only)"""
    from .forms import RoomForm
    
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully!')
            return redirect('hms:room_list')
    else:
        form = RoomForm()
    
    return render(request, 'hms/admin/room_form.html', {'form': form, 'action': 'Create'})


@login_required
def edit_room(request, pk):
    """Edit room details (admin only)"""
    from .forms import RoomForm
    
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    room = get_object_or_404(Room, pk=pk)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully!')
            return redirect('hms:room_list')
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'hms/admin/room_form.html', {'form': form, 'action': 'Edit', 'room': room})


@login_required
def delete_room(request, pk):
    """Delete a room (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('hms:room_list')
    
    room = get_object_or_404(Room, pk=pk)
    room_number = room.room_number
    room.delete()
    messages.success(request, f'Room {room_number} deleted successfully!')
    return redirect('hms:room_list')


@login_required
def room_assignments(request):
    """View all room assignments (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    assignments = RoomAssignment.objects.filter(is_active=True).select_related('student__user', 'room')
    
    context = {
        'assignments': assignments,
        'total_assigned': assignments.count(),
    }
    
    return render(request, 'hms/admin/room_assignments.html', context)


@login_required
def assign_room(request):
    """Assign a student to a room (admin only)"""
    from .forms import RoomAssignmentForm
    
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    if request.method == 'POST':
        form = RoomAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            
            # Check if room has available beds
            room = assignment.room
            if room.available_beds <= 0:
                messages.error(request, f'Room {room.room_number} is full!')
                return render(request, 'hms/admin/room_assignment_form.html', {'form': form})
            
            assignment.save()
            
            # Update student's room_number field
            student = assignment.student
            student.room_number = room.room_number
            student.save()
            
            messages.success(request, f'{student.user.get_full_name()} assigned to Room {room.room_number}!')
            return redirect('hms:room_assignments')
    else:
        form = RoomAssignmentForm()
    
    return render(request, 'hms/admin/room_assignment_form.html', {'form': form})


@login_required
def room_change_requests(request):
    """View all room change requests (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    requests_list = RoomChangeRequest.objects.all().select_related('student__user', 'current_room', 'requested_room')
    
    context = {
        'change_requests': requests_list,
        'pending_count': requests_list.filter(status='pending').count(),
    }
    
    return render(request, 'hms/admin/room_change_requests.html', context)


@login_required
def approve_room_change(request, pk):
    """Approve/reject a room change request (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    room_change = get_object_or_404(RoomChangeRequest, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')
        
        if action == 'approve':
            room_change.status = 'approved'
            room_change.admin_notes = admin_notes
            room_change.reviewed_by = request.user
            room_change.save()
            
            # Create new assignment if there's a requested room
            if room_change.requested_room:
                # Deactivate old assignment
                RoomAssignment.objects.filter(student=room_change.student, is_active=True).update(is_active=False, checkout_date=timezone.now().date())
                
                # Create new assignment
                RoomAssignment.objects.create(
                    student=room_change.student,
                    room=room_change.requested_room,
                    assigned_date=timezone.now().date(),
                    is_active=True
                )
                
                # Update student's room_number
                room_change.student.room_number = room_change.requested_room.room_number
                room_change.student.save()
            
            messages.success(request, f'Room change request approved for {room_change.student.user.get_full_name()}!')
        
        elif action == 'reject':
            room_change.status = 'rejected'
            room_change.admin_notes = admin_notes
            room_change.reviewed_by = request.user
            room_change.save()
            messages.info(request, 'Room change request rejected.')
        
        return redirect('hms:room_change_requests')
    
    return render(request, 'hms/admin/approve_room_change.html', {'room_change': room_change})


@login_required
def student_request_room_change(request):
    """Student submits a room change request"""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('hms:student_dashboard')
    
    from .forms import RoomChangeRequestForm
    
    # Get student's current room
    current_assignment = RoomAssignment.objects.filter(student=student, is_active=True).first()
    
    if request.method == 'POST':
        form = RoomChangeRequestForm(request.POST)
        if form.is_valid():
            room_change = form.save(commit=False)
            room_change.student = student
            room_change.current_room = current_assignment.room if current_assignment else None
            room_change.save()
            
            messages.success(request, 'Room change request submitted successfully!')
            return redirect('hms:student_dashboard')
    else:
        form = RoomChangeRequestForm()
    
    context = {
        'form': form,
        'current_room': current_assignment.room if current_assignment else None,
    }
    
    return render(request, 'hms/student/room_change_request_form.html', context)


# ==================== LEAVE REQUESTS ====================

@login_required
def submit_leave_request(request):
    """Student submits a leave request"""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('hms:student_dashboard')
    
    from .forms import LeaveRequestForm
    
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.student = student
            leave_request.save()
            
            # Notify admin
            from .notifications import notify_leave_request_submitted
            notify_leave_request_submitted(leave_request)
            
            messages.success(request, 'Leave request submitted successfully! Awaiting approval.')
            return redirect('hms:student_leave_list')
    else:
        form = LeaveRequestForm()
    
    return render(request, 'hms/student/leave_request_form.html', {'form': form})


@login_required
def student_leave_list(request):
    """Student views their leave requests"""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('hms:student_dashboard')
    
    leave_requests = LeaveRequest.objects.filter(student=student).order_by('-created_at')
    
    context = {
        'leave_requests': leave_requests,
        'pending_count': leave_requests.filter(status='pending').count(),
    }
    
    return render(request, 'hms/student/leave_list.html', context)

@login_required
def delete_leave_request(request, pk):
    """Student cancels their pending leave request"""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('hms:student_dashboard')
    
    leave_req = get_object_or_404(LeaveRequest, pk=pk, student=student)
    
    if leave_req.status != 'pending':
        messages.error(request, "Cannot cancel leave request that has already been processed.")
        return redirect('hms:student_leave_list')
        
    if request.method == 'POST':
        leave_req.delete()
        messages.success(request, "Leave request cancelled successfully.")
        
    return redirect('hms:student_leave_list')


@login_required
def manage_leave_requests(request):
    """Admin views all leave requests"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    leave_requests = LeaveRequest.objects.all().select_related('student__user').order_by(
        models.Case(
            models.When(status='pending', then=0),
            models.When(status='approved', then=1),
            models.When(status='rejected', then=2),
            default=3,
        ),
        '-created_at'
    )
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        leave_requests = leave_requests.filter(status=status_filter)
    
    context = {
        'leave_requests': leave_requests,
        'pending_count': LeaveRequest.objects.filter(status='pending').count(),
        'status_filter': status_filter,
    }
    
    return render(request, 'hms/admin/leave_requests.html', context)


@login_required
def approve_leave_request(request, pk):
    """Admin approves/rejects a leave request"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    from .forms import LeaveApprovalForm
    
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    if request.method == 'POST':
        form = LeaveApprovalForm(request.POST, instance=leave_request)
        if form.is_valid():
            leave_req = form.save(commit=False)
            leave_req.reviewed_by = request.user
            leave_req.reviewed_at = timezone.now()
            leave_req.save()
            
            # If approved, create AwayPeriod automatically
            if leave_req.status == 'approved':
                AwayPeriod.objects.create(
                    student=leave_req.student,
                    start_date=leave_req.start_date,
                    end_date=leave_req.end_date
                )
                messages.success(request, f'Leave request approved for {leave_req.student.user.get_full_name()}. Away period created.')
            else:
                messages.info(request, f'Leave request updated to {leave_req.get_status_display()}.')
            
            # Notify student
            from .notifications import notify_leave_request_status
            notify_leave_request_status(leave_req)
            
            return redirect('hms:manage_leave_requests')
    else:
        form = LeaveApprovalForm(instance=leave_request)
    
    return render(request, 'hms/admin/approve_leave.html', {'form': form, 'leave_request': leave_request})


# ==================== ANALYTICS DASHBOARD ====================

@login_required
def analytics_dashboard(request):
    """Comprehensive analytics dashboard for admins"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    import json
    from django.db.models import Count, Q
    from django.db.models.functions import TruncDate
    
    today = date.today()
    week_start = today - timedelta(days=6)
    month_start = today - timedelta(days=29)
    
    # ==================== SUMMARY STATS ====================
    total_students = Student.objects.count()
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(is_available=True).count()
    
    # Today's meal stats
    today_meals = Meal.objects.filter(date=today)
    today_breakfast = today_meals.filter(breakfast=True).count()
    today_supper = today_meals.filter(supper=True).count()
    today_away = today_meals.filter(away=True).count()
    today_confirmed = today_meals.count()
    
    # Active leave requests
    active_leaves = LeaveRequest.objects.filter(
        status='approved',
        start_date__lte=today,
        end_date__gte=today
    ).count()
    
    # Pending items
    pending_maintenance = MaintenanceRequest.objects.filter(status='pending').count()
    pending_leaves = LeaveRequest.objects.filter(status='pending').count()
    
    # ==================== WEEKLY MEAL TRENDS ====================
    weekly_labels = []
    weekly_breakfast = []
    weekly_supper = []
    weekly_early = []
    weekly_away = []
    
    for i in range(7):
        d = week_start + timedelta(days=i)
        weekly_labels.append(d.strftime('%a'))
        stats = Meal.objects.filter(date=d).aggregate(
            breakfast=Count('id', filter=Q(breakfast=True)),
            supper=Count('id', filter=Q(supper=True)),
            early=Count('id', filter=Q(early=True)),
            away=Count('id', filter=Q(away=True)),
        )
        weekly_breakfast.append(stats['breakfast'] or 0)
        weekly_supper.append(stats['supper'] or 0)
        weekly_early.append(stats['early'] or 0)
        weekly_away.append(stats['away'] or 0)
    
    # ==================== MONTHLY TRENDS ====================
    monthly_labels = []
    monthly_breakfast = []
    monthly_supper = []
    
    for i in range(30):
        d = month_start + timedelta(days=i)
        monthly_labels.append(d.strftime('%m/%d'))
        stats = Meal.objects.filter(date=d).aggregate(
            breakfast=Count('id', filter=Q(breakfast=True)),
            supper=Count('id', filter=Q(supper=True)),
        )
        monthly_breakfast.append(stats['breakfast'] or 0)
        monthly_supper.append(stats['supper'] or 0)
    
    # ==================== MAINTENANCE STATS ====================
    maintenance_by_status = {
        'pending': MaintenanceRequest.objects.filter(status='pending').count(),
        'in_progress': MaintenanceRequest.objects.filter(status='in_progress').count(),
        'resolved': MaintenanceRequest.objects.filter(status='resolved').count(),
    }
    
    maintenance_by_priority = {
        'low': MaintenanceRequest.objects.filter(priority='low').count(),
        'medium': MaintenanceRequest.objects.filter(priority='medium').count(),
        'high': MaintenanceRequest.objects.filter(priority='high').count(),
        'critical': MaintenanceRequest.objects.filter(priority='critical').count(),
    }
    
    # ==================== LEAVE REQUEST STATS ====================
    leave_by_status = {
        'pending': LeaveRequest.objects.filter(status='pending').count(),
        'approved': LeaveRequest.objects.filter(status='approved').count(),
        'rejected': LeaveRequest.objects.filter(status='rejected').count(),
    }
    
    leave_by_type = {}
    for leave_type_code, leave_type_name in LeaveRequest.LEAVE_TYPES:
        leave_by_type[leave_type_name] = LeaveRequest.objects.filter(leave_type=leave_type_code).count()
    
    # ==================== ROOM OCCUPANCY ====================
    room_stats = {
        'total': total_rooms,
        'available': available_rooms,
        'occupied': total_rooms - available_rooms,
        'occupancy_rate': round((total_rooms - available_rooms) / total_rooms * 100, 1) if total_rooms > 0 else 0
    }
    
    # Room by type
    room_by_type = {}
    for room_type_code, room_type_name in Room.ROOM_TYPES:
        room_by_type[room_type_name] = Room.objects.filter(room_type=room_type_code).count()
    
    # ==================== RECENT ACTIVITY ====================
    recent_maintenance = MaintenanceRequest.objects.select_related('student__user').order_by('-created_at')[:5]
    recent_leaves = LeaveRequest.objects.select_related('student__user').order_by('-created_at')[:5]
    recent_announcements = Announcement.objects.order_by('-created_at')[:5]
    
    # ==================== CHART DATA JSON ====================
    chart_data = {
        'weekly': {
            'labels': weekly_labels,
            'breakfast': weekly_breakfast,
            'supper': weekly_supper,
            'early': weekly_early,
            'away': weekly_away,
        },
        'monthly': {
            'labels': monthly_labels,
            'breakfast': monthly_breakfast,
            'supper': monthly_supper,
        },
        'maintenance_status': maintenance_by_status,
        'maintenance_priority': maintenance_by_priority,
        'leave_status': leave_by_status,
        'room_occupancy': room_stats,
    }
    
    context = {
        'today': today,
        # Summary stats
        'total_students': total_students,
        'today_breakfast': today_breakfast,
        'today_supper': today_supper,
        'today_away': today_away,
        'today_confirmed': today_confirmed,
        'active_leaves': active_leaves,
        'pending_maintenance': pending_maintenance,
        'pending_leaves': pending_leaves,
        # Room stats
        'room_stats': room_stats,
        'room_by_type': room_by_type,
        # Recent activity
        'recent_maintenance': recent_maintenance,
        'recent_leaves': recent_leaves,
        'recent_announcements': recent_announcements,
        # Chart data
        'chart_data_json': json.dumps(chart_data),
        'leave_by_type': leave_by_type,
    }
    
    return render(request, 'hms/admin/analytics_dashboard.html', context)


@login_required
def visitor_management(request):
    """View to list active visitors and check them in/out"""
    # Only staff can manage visitors
    if not request.user.is_staff and not request.user.student_profile.is_warden:
        messages.error(request, "You do not have permission to access visitor management.")
        return redirect('hms:student_dashboard')
    
    # Handle Check-In Form Submission
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.created_by = request.user
            visitor.save()
            messages.success(request, f"Visitor {visitor.name} checked in successfully.")
            return redirect('hms:visitor_management')
    else:
        form = VisitorForm()
    
    # Get active visitors
    active_visitors = Visitor.objects.filter(is_active=True).order_by('-check_in_time')
    
    # Get recent history (limited to 50 for performance)
    visitor_history = Visitor.objects.filter(is_active=False).order_by('-check_out_time')[:50]
    
    context = {
        'form': form,
        'active_visitors': active_visitors,
        'visitor_history': visitor_history,
    }
    
    return render(request, 'hms/admin/visitor_management.html', context)

@login_required
def checkout_visitor(request, visitor_id):
    """View to check out a visitor"""
    if not request.user.is_staff and not request.user.student_profile.is_warden:
        messages.error(request, "Permission denied.")
        return redirect('hms:student_dashboard')
        
    visitor = get_object_or_404(Visitor, id=visitor_id)
    
    if visitor.is_active:
        visitor.check_out()
        messages.success(request, f"Visitor {visitor.name} has been checked out.")
    else:
        messages.warning(request, "Visitor is already checked out.")
        
    return redirect('hms:visitor_management')


# ==================== EVENT MANAGEMENT ====================

@login_required
def events_list(request):
    """List all published events for students"""
    today = date.today()
    
    # Get all published events
    upcoming_events = Event.objects.filter(
        is_published=True,
        event_date__gte=today
    ).order_by('event_date', 'start_time')
    
    past_events = Event.objects.filter(
        is_published=True,
        event_date__lt=today
    ).order_by('-event_date', '-start_time')[:10]
    
    # Get student's RSVPs if user is a student
    my_rsvps = {}
    
    # Convert queryset to list so we can attach attributes
    upcoming_events = list(upcoming_events)
    
    if hasattr(request.user, 'student_profile'):
        student = request.user.student_profile
        rsvps = EventRSVP.objects.filter(student=student).select_related('event')
        my_rsvps = {rsvp.event_id: rsvp for rsvp in rsvps}
        
        # Attach RSVP status directly to event objects
        for event in upcoming_events:
            event.user_rsvp = my_rsvps.get(event.id)
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'my_rsvps': my_rsvps,
        'today': today,
    }
    return render(request, 'hms/events/event_list.html', context)


@login_required
def event_detail(request, pk):
    """View single event details"""
    event = get_object_or_404(Event, pk=pk)
    
    # Check if user has RSVPed
    my_rsvp = None
    can_rsvp = False
    
    if hasattr(request.user, 'student_profile'):
        student = request.user.student_profile
        try:
            my_rsvp = EventRSVP.objects.get(event=event, student=student)
        except EventRSVP.DoesNotExist:
            pass
        
        # Can RSVP if event requires RSVP, isn't full, and isn't in the past
        can_rsvp = event.requires_rsvp and not event.is_past and not event.is_full
    
    # Get all attend RSVPs for attendance list
    attending_rsvps = event.rsvps.filter(status='attending').select_related('student__user')
    
    context = {
        'event': event,
        'my_rsvp': my_rsvp,
        'can_rsvp': can_rsvp,
        'attending_rsvps': attending_rsvps,
    }
    return render(request, 'hms/events/event_detail.html', context)


@login_required
def event_rsvp(request, pk):
    """Student RSVPs to an event"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Only students can RSVP to events.")
        return redirect('hms:events_list')
    
    event = get_object_or_404(Event, pk=pk)
    student = request.user.student_profile
    
    # Check if event allows RSVP
    if not event.requires_rsvp:
        messages.info(request, "This event does not require RSVP.")
        return redirect('hms:event_detail', pk=pk)
    
    # Check if event is full
    if event.is_full:
        messages.error(request, "Sorry, this event is full.")
        return redirect('hms:event_detail', pk=pk)
    
    # Check if event is in the past
    if event.is_past:
        messages.error(request, "Cannot RSVP to past events.")
        return redirect('hms:event_detail', pk=pk)
    
    if request.method == 'POST':
        # Get or create RSVP
        rsvp, created = EventRSVP.objects.get_or_create(
            event=event,
            student=student
        )
        
        form = EventRSVPForm(request.POST, instance=rsvp)
        if form.is_valid():
            form.save()
            if created:
                messages.success(request, f"Successfully RSVPed to {event.title}!")
            else:
                messages.success(request, "RSVP updated successfully!")
            return redirect('hms:event_detail', pk=pk)
    else:
        try:
            rsvp = EventRSVP.objects.get(event=event, student=student)
            form = EventRSVPForm(instance=rsvp)
        except EventRSVP.DoesNotExist:
            form = EventRSVPForm()
    
    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'hms/events/event_rsvp.html', context)


@login_required
def my_events(request):
    """Student views their event RSVPs"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Access denied.")
        return redirect('hms:events_list')
    
    student = request.user.student_profile
    today = date.today()
    
    # Get upcoming events the student has RSVPed to
    upcoming_rsvps = EventRSVP.objects.filter(
        student=student,
        event__event_date__gte=today
    ).select_related('event').order_by('event__event_date', 'event__start_time')
    
    # Get past events
    past_rsvps = EventRSVP.objects.filter(
        student=student,
        event__event_date__lt=today
    ).select_related('event').order_by('-event__event_date', '-event__start_time')[:10]
    
    context = {
        'upcoming_rsvps': upcoming_rsvps,
        'past_rsvps': past_rsvps,
    }
    return render(request, 'hms/events/my_events.html', context)


@login_required
def manage_events(request):
    """Admin manages all events"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:events_list')
    
    today = date.today()
    
    # Get all events
    upcoming_events = Event.objects.filter(
        event_date__gte=today
    ).order_by('event_date', 'start_time')
    
    past_events = Event.objects.filter(
        event_date__lt=today
    ).order_by('-event_date', '-start_time')[:20]
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'hms/events/manage_events.html', context)


@login_required
def create_event(request):
    """Admin creates a new event"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:events_list')
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, f"Event '{event.title}' created successfully!")
            return redirect('hms:manage_events')
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'title': 'Create New Event',
    }
    return render(request, 'hms/events/event_form.html', context)


@login_required
def edit_event(request, pk):
    """Admin edits an event"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:events_list')
    
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f"Event '{event.title}' updated successfully!")
            return redirect('hms:manage_events')
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'title': 'Edit Event',
    }
    return render(request, 'hms/events/event_form.html', context)


@login_required
def delete_event(request, pk):
    """Admin deletes an event"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:events_list')
    
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('hms:manage_events')
    
    event = get_object_or_404(Event, pk=pk)
    event_title = event.title
    event.delete()
    messages.success(request, f"Event '{event_title}' deleted successfully!")
    return redirect('hms:manage_events')


@login_required
def event_attendees(request, pk):
    """Admin views event attendees and marks attendance"""
    if not request.user.is_staff:
        messages.error(request,  "Access denied. Admin only.")
        return redirect('hms:events_list')
    
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        # Mark attendance
        rsvp_id = request.POST.get('rsvp_id')
        attended = request.POST.get('attended') == 'on'
        
        try:
            rsvp = EventRSVP.objects.get(id=rsvp_id, event=event)
            rsvp.attended = attended
            rsvp.save()
            messages.success(request, "Attendance updated!")
        except EventRSVP.DoesNotExist:
            messages.error(request, "RSVP not found.")
    
    # Get all RSVPs for this event
    rsvps = event.rsvps.select_related('student__user').order_by('student__user__first_name')
    
    # Statistics
    total_rsvps = rsvps.count()
    attending_count = rsvps.filter(status='attending').count()
    attended_count = rsvps.filter(attended=True).count()
    
    context = {
        'event': event,
        'rsvps': rsvps,
        'total_rsvps': total_rsvps,
        'attending_count': attending_count,
        'attended_count': attended_count,
    }
    return render(request, 'hms/events/event_attendees.html', context)

# ==================== Payment & M-Pesa ====================

@login_required
def pay_accommodation(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        
        # Basic validation
        if not phone or not amount:
            messages.error(request, "Please provide phone number and amount")
            return redirect('hms:pay_accommodation')

        # Save pending payment
        try:
            student = request.user.student_profile
        except Student.DoesNotExist:
            messages.error(request, "Student profile not found.")
            return redirect('hms:dashboard')

        payment = Payment.objects.create(
            student=student,
            amount=amount,
            phone_number=phone,
            status='Pending'
        )
        
        # Initiate STK Push
        mpesa = MpesaClient()
        # Ensure callback URL is accessible from internet (e.g. ngrok) for local dev
        callback_url = settings.MPESA_CALLBACK_URL
        response = mpesa.stk_push(phone, amount, "Accommodation", callback_url)
        
        if response.get('ResponseCode') == '0':
            payment.checkout_request_id = response.get('CheckoutRequestID')
            payment.save()
            messages.success(request, f"STK Push initiated to {phone}. Check your phone to complete payment.")
        else:
            payment.status = 'Failed'
            payment.description = response.get('ResponseDescription', 'Unknown Error')
            payment.save()
            messages.error(request, f"Payment initiation failed: {payment.description}")
            
        return redirect('hms:payment_history')
        
    return render(request, 'hms/student/pay_accommodation.html')

@login_required
def payment_history(request):
    try:
        student = request.user.student_profile
        payments = Payment.objects.filter(student=student).order_by('-created_at')
    except Student.DoesNotExist:
        payments = []
    return render(request, 'hms/student/payment_history.html', {'payments': payments})

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Log raw data for debugging if needed
            # print(data)
            
            stk_callback = data.get('Body', {}).get('stkCallback', {})
            result_code = stk_callback.get('ResultCode')
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            result_desc = stk_callback.get('ResultDesc')
            
            if not checkout_request_id:
                return JsonResponse({'status': 'error', 'message': 'No CheckoutRequestID'}, status=400)

            try:
                payment = Payment.objects.get(checkout_request_id=checkout_request_id)
            except Payment.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Payment not found'}, status=404)

            if result_code == 0:
                payment.status = 'Completed'
                payment.description = 'Success'
                # Extract receipt no
                meta = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                for item in meta:
                    if item.get('Name') == 'MpesaReceiptNumber':
                        payment.transaction_id = item.get('Value')
                
                # Send Notification
                Notification.objects.create(
                    user=payment.student.user,
                    title="Payment Received",
                    message=f"We received your payment of KES {payment.amount}. Ref: {payment.transaction_id}",
                    link="/student/payment-history/"
                )
            else:
                payment.status = 'Failed'
                payment.description = result_desc

            payment.save()
        except Exception as e:
            print(f"Callback Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'only post'}, status=400)

@login_required
def check_payment_status(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, student=request.user.student_profile)
    
    if payment.status == 'Completed':
        messages.info(request, "Payment is already completed.")
        return redirect('hms:payment_history')
        
    if not payment.checkout_request_id:
        messages.error(request, "Cannot verify this payment (No CheckoutRequestID).")
        return redirect('hms:payment_history')

    mpesa = MpesaClient()
    response = mpesa.stk_push_query(payment.checkout_request_id)
    
    if response.get('ResponseCode') == '0':
        result_code = response.get('ResultCode')
        if result_code == '0':
            payment.status = 'Completed'
            payment.description = response.get('ResultDesc', 'Verified Manually')
            payment.save()
            
            Notification.objects.create(
                user=request.user, 
                title="Payment Verified",
                message=f"Manual verification successful for KES {payment.amount}.",
                link="/student/payment-history/"
            )
            
            messages.success(request, "Payment verified successfully!")
        else:
            if result_code in ['1032', '1037', '1']:
                payment.status = 'Failed'
                payment.description = response.get('ResultDesc')
                payment.save()
            messages.warning(request, f"Payment status: {response.get('ResultDesc')}")
    else:
        messages.error(request, f"Query failed: {response.get('ResponseDescription', response.get('errorMessage'))}")
        
    return redirect('hms:payment_history')
