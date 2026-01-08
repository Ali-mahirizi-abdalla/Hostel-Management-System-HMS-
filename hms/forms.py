from django import forms
from django.contrib.auth.models import User
from .models import (Student, AwayPeriod, Activity, Document, Message, MaintenanceRequest,
                     Room, RoomAssignment, RoomChangeRequest, LeaveRequest)

class StudentRegistrationForm(forms.ModelForm):
    # User fields
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'w-full p-2 rounded bg-gray-50 border border-gray-300 text-gray-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'w-full p-2 rounded bg-gray-50 border border-gray-300 text-gray-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'w-full p-2 rounded bg-gray-50 border border-gray-300 text-gray-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'}))
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'w-full p-2 rounded bg-gray-50 border border-gray-300 text-gray-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 rounded bg-gray-50 border border-gray-300 text-gray-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 rounded bg-gray-50 border border-gray-300 text-gray-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'}))

    # Student fields
    university_id = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'w-full p-2 rounded bg-gray-50 border border-gray-300 text-gray-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'w-full p-2 rounded bg-gray-50 border border-gray-300 text-gray-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'}))

    class Meta:
        model = Student
        fields = ['university_id', 'phone']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        # 1. Create the User (triggers post_save signal which creates a Student profile)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        # 2. Get the auto-created student profile
        # The signal in hms/signals.py guarantees this exists for new users
        student = user.student_profile
        
        # 3. Update it with form data
        student.university_id = self.cleaned_data['university_id']
        student.phone = self.cleaned_data['phone']
        
        if commit:
            student.save()
            
        return student

class AwayModeForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded'}))

    class Meta:
        model = AwayPeriod
        fields = ['start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and start > end:
            raise forms.ValidationError("End date must be after start date.")
        return cleaned_data

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['display_name', 'weekday', 'time', 'description', 'active']
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'weekday': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full p-2 border rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3}),
            'active': forms.CheckboxInput(attrs={'class': 'p-2'}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'file': forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}),
        }

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['timetable']
        widgets = {
            'timetable': forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}),
        }

class RoomSelectionForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['room_number']
        widgets = {
            'room_number': forms.Select(choices=[(str(i), str(i)) for i in range(1, 51)], attrs={'class': 'w-full p-2 border rounded'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500', 
                'rows': 3, 
                'placeholder': 'Type your message...'
            }),
        }

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['title', 'description', 'priority', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all hover:bg-black/30',
                'placeholder': 'e.g., Leaking tap in Room 101'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all hover:bg-black/30',
                'rows': 4,
                'placeholder': 'Describe the issue...'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all hover:bg-black/30'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-teal-500/10 file:text-teal-400 hover:file:bg-teal-500/20 transition-all'
            }),
        }

class MaintenanceStatusForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full bg-black/30 border border-white/20 text-white text-sm rounded-lg focus:ring-purple-500 focus:border-purple-500 block p-2.5'
            }),
        }


# ========== ROOM MANAGEMENT FORMS ==========

class RoomForm(forms.ModelForm):
    """Form for creating and editing rooms"""
    class Meta:
        model = Room
        fields = ['room_number', 'floor', 'block', 'room_type', 'capacity', 'is_available', 'amenities']
        widgets = {
            'room_number': forms.TextInput(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all',
                'placeholder': 'e.g., 101, A-205'
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all',
                'min': '1'
            }),
            'block': forms.TextInput(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all',
                'placeholder': 'e.g., Block A, North Wing'
            }),
            'room_type': forms.Select(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all',
                'min': '1',
                'max': '4'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-teal-600 bg-slate-100 border-slate-300 rounded focus:ring-teal-500 dark:focus:ring-teal-600 dark:ring-offset-slate-800 focus:ring-2 dark:bg-slate-700 dark:border-slate-600'
            }),
            'amenities': forms.Textarea(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all',
                'rows': 3,
                'placeholder': 'AC, Attached Bathroom, Study Table, etc.'
            }),
        }


class RoomAssignmentForm(forms.ModelForm):
    """Form for assigning students to rooms"""
    class Meta:
        model = RoomAssignment
        fields = ['student', 'room', 'bed_number', 'assigned_date', 'notes']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all'
            }),
            'room': forms.Select(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all'
            }),
            'bed_number': forms.NumberInput(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all',
                'min': '1'
            }),
            'assigned_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all',
                'rows': 3,
                'placeholder': 'Optional notes about this assignment'
            }),
        }


class RoomChangeRequestForm(forms.ModelForm):
    """Form for students to request room changes"""
    class Meta:
        model = RoomChangeRequest
        fields = ['requested_room', 'reason']
        widgets = {
            'requested_room': forms.Select(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all',
                'rows': 4,
                'placeholder': 'Please explain why you want to change rooms...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available rooms
        self.fields['requested_room'].queryset = Room.objects.filter(is_available=True)


# ========== LEAVE REQUEST FORMS ==========

class LeaveRequestForm(forms.ModelForm):
    """Form for students to submit leave requests"""
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason', 'contact_during_leave', 'destination']
        widgets = {
            'leave_type': forms.Select(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all',
                'rows': 4,
                'placeholder': 'Please explain the reason for your leave...'
            }),
            'contact_during_leave': forms.TextInput(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all',
                'placeholder': '+254 712 345 678'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all',
                'placeholder': 'e.g., Nairobi, Mombasa'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data


class LeaveApprovalForm(forms.ModelForm):
    """Form for admin to approve/reject leave requests"""
    class Meta:
        model = LeaveRequest
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
            }),
            'admin_notes': forms.Textarea(attrs={
                'class': 'w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-3 text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all',
                'rows': 3,
                'placeholder': 'Optional notes or feedback for the student...'
            }),
        }
