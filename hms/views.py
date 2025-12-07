from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from datetime import date, timedelta, datetime
from .models import StudentProfile, MealConfirmation, ActivitySchedule, Announcement, MealTimingOverride
from .forms import StudentRegistrationForm


# ==================== Authentication Views ====================

def register_student(request):
    """Register a new student"""
    if request.user.is_authenticated:
        return redirect('hms:home')
        
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the hostel.')
            return redirect('hms:student_dashboard')
        else:
            print("REGISTRATION ERRORS:", form.errors)
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'hms/registration/register.html', {'form': form})

def home(request):
    """Home page - redirect based on user role"""
    if request.user.is_authenticated:
        if hasattr(request.user, 'student_profile'):
            return redirect('hms:student_dashboard')
        elif request.user.is_staff:
            return redirect('hms:kitchen_dashboard')
    return redirect('hms:login')


def user_login(request):
    """Login view for all users"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"DEBUG: Login attempt for user '{username}'")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"DEBUG: Authentication successful for '{username}'")
            if not user.is_active:
                print(f"DEBUG: User '{username}' is inactive")
                messages.error(request, 'Your account is inactive.')
                return render(request, 'hms/login.html')

            login(request, user)
            # Redirect based on user role
            if hasattr(user, 'student_profile'):
                return redirect('hms:student_dashboard')
            elif user.is_staff:
                return redirect('hms:kitchen_dashboard')
            else:
                return redirect('hms:student_dashboard')
        else:
            print(f"DEBUG: Authentication failed for '{username}'")
            # Check if user exists to give better debug info (only in console)
            from django.contrib.auth.models import User
            if User.objects.filter(username=username).exists():
                print(f"DEBUG: User '{username}' exists but password mismatch")
            else:
                print(f"DEBUG: User '{username}' does not exist")
                
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'hms/login.html')
    
    return render(request, 'hms/login.html')


def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('hms:login')


# ==================== Student Views ====================

@login_required
def student_dashboard(request):
    """Student dashboard with meal confirmation interface"""
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact admin.')
        return redirect('hms:login')
    
    # Get or create meal confirmation for today and tomorrow
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    today_meals, _ = MealConfirmation.objects.get_or_create(
        student=student_profile,
        date=today,
        defaults={'early_breakfast_needed': student_profile.default_early_breakfast}
    )
    
    tomorrow_meals, _ = MealConfirmation.objects.get_or_create(
        student=student_profile,
        date=tomorrow,
        defaults={'early_breakfast_needed': student_profile.default_early_breakfast}
    )
    
    # Get active announcements
    announcements = Announcement.objects.filter(is_active=True)[:5]
    
    # Get today's activities
    today_activities = ActivitySchedule.objects.filter(
        day_of_week=today.weekday(),
        is_active=True
    )
    
    context = {
        'student': student_profile,
        'today_meals': today_meals,
        'tomorrow_meals': tomorrow_meals,
        'announcements': announcements,
        'today_activities': today_activities,
        'today': today,
        'tomorrow': tomorrow,
    }
    
    return render(request, 'hms/student/dashboard.html', context)


@login_required
def confirm_meals(request):
    """AJAX endpoint to confirm meals"""
    if request.method == 'POST':
        try:
            student_profile = request.user.student_profile
            meal_date = request.POST.get('date')
            # Handle both standard form submission and potential AJAX
            breakfast = request.POST.get('breakfast') in ['on', 'true', 'True', True]
            lunch = request.POST.get('lunch') in ['on', 'true', 'True', True]
            supper = request.POST.get('supper') in ['on', 'true', 'True', True]
            early_breakfast = request.POST.get('early_breakfast') in ['on', 'true', 'True', True]
            
            # Enforce 8:00 AM lock for breakfast/early breakfast
            current_time = datetime.now().time()
            lock_time = time(8, 0)  # 08:00 AM
            
            if meal_date == str(date.today()) and current_time > lock_time:
                # If it's today and past 8 AM, prevent changing breakfast/early breakfast
                # We fetch existing values to preserve them
                existing = MealConfirmation.objects.filter(student=student_profile, date=meal_date).first()
                if existing:
                    breakfast = existing.breakfast
                    early_breakfast = existing.early_breakfast_needed
                else:
                    breakfast = False
                    early_breakfast = False
            
            meal_confirmation, created = MealConfirmation.objects.update_or_create(
                student=student_profile,
                date=meal_date,
                defaults={
                    'breakfast': breakfast,
                    'lunch': lunch,
                    'supper': supper,
                    'early_breakfast_needed': early_breakfast,
                }
            )
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Meals confirmed successfully',
                    'data': {
                        'breakfast': meal_confirmation.breakfast,
                        'lunch': meal_confirmation.lunch,
                        'supper': meal_confirmation.supper,
                        'early_breakfast': meal_confirmation.early_breakfast_needed,
                    }
                })
            else:
                messages.success(request, 'Meals confirmed successfully')
                return redirect('hms:student_dashboard')
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)}, status=400)
            else:
                messages.error(request, f'Error confirming meals: {e}')
                return redirect('hms:student_dashboard')
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
def toggle_away_mode(request):
    """Toggle away mode for student"""
    if request.method == 'POST':
        try:
            student_profile = request.user.student_profile
            action = request.POST.get('action')
            
            if action == 'away':
                from_date = datetime.strptime(request.POST.get('from_date'), '%Y-%m-%d').date()
                to_date = datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d').date()
                student_profile.mark_away(from_date, to_date)
                return JsonResponse({
                    'success': True,
                    'message': f'Marked as away from {from_date} to {to_date}',
                    'is_away': True
                })
            elif action == 'return':
                student_profile.mark_return()
                return JsonResponse({
                    'success': True,
                    'message': 'Welcome back! You can now confirm your meals.',
                    'is_away': False
                })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
def toggle_early_breakfast(request):
    """Toggle early breakfast preference"""
    if request.method == 'POST':
        try:
            student_profile = request.user.student_profile
            meal_date = request.POST.get('date')
            early_breakfast = request.POST.get('early_breakfast') == 'true'
            
            meal_confirmation = MealConfirmation.objects.get(
                student=student_profile,
                date=meal_date
            )
            meal_confirmation.early_breakfast_needed = early_breakfast
            meal_confirmation.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Early breakfast preference updated',
                'early_breakfast': early_breakfast
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
def student_profile(request):
    """Student profile view"""
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found')
        return redirect('hms:login')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_photo' and request.FILES.get('profile_picture'):
            student_profile.profile_picture = request.FILES['profile_picture']
            student_profile.save()
            messages.success(request, 'Profile picture updated!')
            return redirect('hms:student_profile')
            
        elif action == 'update_info':
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            
            student_profile.phone_number = request.POST.get('phone_number')
            student_profile.default_early_breakfast = request.POST.get('default_early_breakfast') == 'on'
            student_profile.save()
            
            messages.success(request, 'Profile information updated!')
            return redirect('hms:student_profile')
    
    # Get meal history
    meal_history = MealConfirmation.objects.filter(
        student=student_profile
    ).order_by('-date')[:30]
    
    context = {
        'student': student_profile,
        'meal_history': meal_history,
    }
    
    return render(request, 'hms/student/profile.html', context)


# ==================== Kitchen Views ====================

@login_required
def kitchen_dashboard(request):
    """Kitchen dashboard with real-time meal counts"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('hms:student_dashboard')
    
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # Get meal counts for today
    today_breakfast = MealConfirmation.get_meal_count(today, 'breakfast')
    today_lunch = MealConfirmation.get_meal_count(today, 'lunch')
    today_supper = MealConfirmation.get_meal_count(today, 'supper')
    today_early_breakfast = MealConfirmation.get_early_breakfast_count(today)
    
    # Get meal counts for tomorrow
    tomorrow_breakfast = MealConfirmation.get_meal_count(tomorrow, 'breakfast')
    tomorrow_lunch = MealConfirmation.get_meal_count(tomorrow, 'lunch')
    tomorrow_supper = MealConfirmation.get_meal_count(tomorrow, 'supper')
    tomorrow_early_breakfast = MealConfirmation.get_early_breakfast_count(tomorrow)
    
    # Get total students
    total_students = StudentProfile.objects.count()
    
    # Get students away
    students_away = StudentProfile.objects.filter(is_away=True).count()
    
    # Get confirmed students for today
    confirmed_students = MealConfirmation.objects.filter(date=today).select_related('student', 'student__user')
    
    context = {
        'today': today,
        'tomorrow': tomorrow,
        'today_breakfast': today_breakfast,
        'today_lunch': today_lunch,
        'today_supper': today_supper,
        'today_early_breakfast': today_early_breakfast,
        'tomorrow_breakfast': tomorrow_breakfast,
        'tomorrow_lunch': tomorrow_lunch,
        'tomorrow_supper': tomorrow_supper,
        'tomorrow_early_breakfast': tomorrow_early_breakfast,
        'total_students': total_students,
        'students_away': students_away,
        'confirmed_students': confirmed_students,
    }
    
    return render(request, 'hms/kitchen/dashboard.html', context)


@login_required
def meal_count_api(request):
    """JSON API for real-time meal counts"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    meal_date_str = request.GET.get('date', str(date.today()))
    
    # Try multiple date formats
    meal_date = None
    date_formats = ['%Y-%m-%d', '%b. %d, %Y', '%B %d, %Y', '%d/%m/%Y', '%m/%d/%Y']
    for fmt in date_formats:
        try:
            meal_date = datetime.strptime(meal_date_str, fmt).date()
            break
        except ValueError:
            continue
    
    # Fallback to today if no format matches
    if meal_date is None:
        meal_date = date.today()
    
    data = {
        'date': str(meal_date),
        'breakfast': MealConfirmation.get_meal_count(meal_date, 'breakfast'),
        'lunch': MealConfirmation.get_meal_count(meal_date, 'lunch'),
        'supper': MealConfirmation.get_meal_count(meal_date, 'supper'),
        'early_breakfast': MealConfirmation.get_early_breakfast_count(meal_date),
        'total_students': StudentProfile.objects.count(),
        'students_away': StudentProfile.objects.filter(is_away=True).count(),
    }
    
    return JsonResponse(data)


@login_required
def early_breakfast_list(request):
    """List of students needing early breakfast"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('hms:student_dashboard')
    
    meal_date = request.GET.get('date', str(date.today()))
    meal_date = datetime.strptime(meal_date, '%Y-%m-%d').date()
    
    students = MealConfirmation.get_early_breakfast_students(meal_date)
    
    context = {
        'students': students,
        'meal_date': meal_date,
    }
    
    return render(request, 'hms/kitchen/early_breakfast.html', context)


@login_required
def daily_report(request):
    """Daily meal report for kitchen"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('hms:student_dashboard')
    
    meal_date = request.GET.get('date', str(date.today()))
    meal_date = datetime.strptime(meal_date, '%Y-%m-%d').date()
    
    # Get all meal confirmations for the date
    confirmations = MealConfirmation.objects.filter(date=meal_date).select_related('student__user')
    
    # Calculate statistics
    breakfast_count = confirmations.filter(breakfast=True).count()
    lunch_count = confirmations.filter(lunch=True).count()
    supper_count = confirmations.filter(supper=True).count()
    early_breakfast_count = confirmations.filter(breakfast=True, early_breakfast_needed=True).count()
    
    context = {
        'meal_date': meal_date,
        'confirmations': confirmations,
        'breakfast_count': breakfast_count,
        'lunch_count': lunch_count,
        'supper_count': supper_count,
        'early_breakfast_count': early_breakfast_count,
        'total_students': StudentProfile.objects.count(),
    }
    
    return render(request, 'hms/kitchen/daily_report.html', context)


# ==================== Admin/Warden Views ====================

@login_required
def admin_dashboard(request):
    """Admin dashboard overview"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('hms:student_dashboard')
    
    total_students = StudentProfile.objects.count()
    students_away = StudentProfile.objects.filter(is_away=True).count()
    active_announcements = Announcement.objects.filter(is_active=True).count()
    activities_count = ActivitySchedule.objects.filter(is_active=True).count()
    
    # Recent announcements
    recent_announcements = Announcement.objects.all()[:5]
    
    context = {
        'total_students': total_students,
        'students_away': students_away,
        'active_announcements': active_announcements,
        'activities_count': activities_count,
        'recent_announcements': recent_announcements,
    }
    
    return render(request, 'hms/admin/dashboard.html', context)


@login_required
def manage_activities(request):
    """Manage activity schedules"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('hms:student_dashboard')
    
    activities = ActivitySchedule.objects.all()
    
    context = {
        'activities': activities,
    }
    
    return render(request, 'hms/admin/activities.html', context)


@login_required
def manage_announcements(request):
    """Manage announcements"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('hms:student_dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        priority = request.POST.get('priority', 'medium')
        
        Announcement.objects.create(
            title=title,
            message=message,
            priority=priority,
            created_by=request.user
        )
        messages.success(request, 'Announcement created successfully')
        return redirect('hms:manage_announcements')
    
    announcements = Announcement.objects.all()
    
    context = {
        'announcements': announcements,
    }
    
    return render(request, 'hms/admin/announcements.html', context)


@login_required
def manage_students(request):
    """Manage students"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('hms:student_dashboard')
    
    students = StudentProfile.objects.all().select_related('user')
    
    context = {
        'students': students,
    }
    
    return render(request, 'hms/admin/students.html', context)


@login_required
def export_meals_csv(request):
    """Export meal confirmations to CSV"""
    if not request.user.is_staff:
        return HttpResponseForbidden("Access denied")

    import csv
    
    meal_date_str = request.GET.get('date', str(date.today()))
    try:
        meal_date = datetime.strptime(meal_date_str, '%Y-%m-%d').date()
    except ValueError:
        meal_date = date.today()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="meals_{meal_date}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Username/ID', 'Room', 'Breakfast', 'Early Breakfast', 'Lunch', 'Supper'])

    confirmations = MealConfirmation.objects.filter(date=meal_date).select_related('student', 'student__user')

    for conf in confirmations:
        writer.writerow([
            conf.student.user.get_full_name(),
            conf.student.user.username,
            conf.student.room_number,
            'Yes' if conf.breakfast else 'No',
            'Yes' if conf.early_breakfast_needed else 'No',
            'Yes' if conf.lunch else 'No',
            'Yes' if conf.supper else 'No',
        ])

    return response
