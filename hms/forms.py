# hms/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import StudentProfile, MealConfirmation, ActivitySchedule, Announcement
from datetime import date  # Add this import for date handling

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['room_number', 'phone_number', 'profile_picture']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    room_number = forms.CharField(max_length=10, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                room_number=self.cleaned_data['room_number'],
                phone_number=self.cleaned_data['phone_number']
            )
        return user

class MealConfirmationForm(forms.ModelForm):
    class Meta:
        model = MealConfirmation
        fields = ['breakfast', 'lunch', 'supper', 'early_breakfast_needed']
        widgets = {
            'breakfast': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lunch': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'supper': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'early_breakfast_needed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# class ActivityForm(forms.ModelForm):
#     class Meta:
#         model = Activity
#         fields = '__all__'
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 3}),
#             'start_time': forms.TimeInput(attrs={'type': 'time'}),
#             'end_time': forms.TimeInput(attrs={'type': 'time'}),
#         }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message', 'is_active']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

# class KitchenNoteForm(forms.ModelForm):
#     class Meta:
#         model = KitchenNote
#         fields = ['title', 'content', 'is_important']
#         widgets = {
#             'content': forms.Textarea(attrs={'rows': 4}),
#         }

# class SpecialMealRequestForm(forms.ModelForm):
#     class Meta:
#         model = SpecialMealRequest
#         fields = ['meal_type', 'date', 'notes']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'}),
#             'notes': forms.Textarea(attrs={'rows': 2}),
#         }

class AwayStatusForm(forms.Form):
    is_away = forms.BooleanField(
        label='I will be away from the hostel',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    away_from_date = forms.DateField(
        label='From',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    away_to_date = forms.DateField(
        label='To',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    reason = forms.CharField(
        label='Reason (optional)',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        is_away = cleaned_data.get('is_away')
        away_from_date = cleaned_data.get('away_from_date')
        away_to_date = cleaned_data.get('away_to_date')
        
        if is_away:
            if not away_from_date or not away_to_date:
                raise forms.ValidationError('Please provide both start and end dates for your away period.')
            
            if away_from_date < date.today():
                raise forms.ValidationError('Start date cannot be in the past.')
                
            if away_to_date < away_from_date:
                raise forms.ValidationError('End date must be after start date.')
        
        return cleaned_data