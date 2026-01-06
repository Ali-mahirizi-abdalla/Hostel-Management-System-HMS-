from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Student, Meal, Activity, AwayPeriod, Announcement
from .forms import StudentRegistrationForm, AwayModeForm
from datetime import date, datetime, time, timedelta
from django.db import transaction, models
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseForbidden

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
    
    context = {
        'student': student,
        'meal_history': meal_history
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
        # Simple update for demo
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        student.university_id = request.POST.get('university_id')
        student.phone = request.POST.get('phone')
        student.save()
        
        messages.success(request, 'Student profile updated!')
        return redirect('hms:manage_students')
    
    return render(request, 'hms/admin/student_details.html', {'student': student, 'edit_mode': True})

@login_required
def delete_student(request, user_id):
    """Delete student (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('hms:student_dashboard')
        
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "Student deleted successfully.")
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
        
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    messages.success(request, "Announcement deleted successfully.")
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
        
        Announcement.objects.create(
            title=title,
            content=content,
            priority=priority,
            created_by=request.user
        )
        messages.success(request, 'Announcement created successfully!')
        return redirect('hms:manage_announcements')
    
    return render(request, 'hms/admin/announcement_form.html')

# ==================== Activities ====================

@login_required
def activities_list(request):
    """View all activities"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect('hms:student_dashboard')
    
    activities = Activity.objects.filter(active=True).order_by('weekday', 'time')
    context = {
        'activities': activities
    }
    return render(request, 'hms/admin/activities.html', context)
