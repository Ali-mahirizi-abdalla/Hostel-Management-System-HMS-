from django import forms
from django.contrib.auth.models import User
from .models import Student, AwayPeriod, Activity

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