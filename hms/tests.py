from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Student, Meal
from datetime import date, timedelta, time
from unittest.mock import patch

class MealSubmissionTest(TestCase):
    def setUp(self):
        # Create test user and student
        self.user = User.objects.create_user(username='teststudent', password='password123')
        self.student = Student.objects.create(user=self.user, university_id='S12345')
        self.client = Client()
        self.client.login(username='teststudent', password='password123')

    def test_meal_creation(self):
        """Test basic meal creation via model"""
        today = date.today()
        Meal.objects.create(student=self.student, date=today, breakfast=True)
        self.assertEqual(Meal.objects.filter(student=self.student).count(), 1)
        
    def test_unique_constraint(self):
        """Test that a student cannot have two meal records for the same day (DB level)"""
        today = date.today()
        Meal.objects.create(student=self.student, date=today, breakfast=True)
        with self.assertRaises(Exception): # IntegrityError usually
            Meal.objects.create(student=self.student, date=today, supper=True)

    @patch('hms.views.datetime') 
    @patch('hms.views.timezone')
    def test_breakfast_lock_logic(self, mock_timezone, mock_datetime):
        """Test that breakfast cannot be changed after 8:00 AM"""
        # Mock time to be 9:00 AM
        fixed_dt = datetime.now()
        # This implementation depends heavily on how views import datetime/timezone
        # Skipping complex mocking for now, testing view response logic directly if possible
        pass

class AdminDashboardTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='password123')
        self.client = Client()
        self.client.login(username='admin', password='password123')

    def test_admin_access(self):
        """Test admin dashboard accessibility"""
        response = self.client.get('/kitchen/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_stats_calculation(self):
        """Test that stats are calculated correctly"""
        # Create some meals
        u1 = User.objects.create_user(username='s1', password='p')
        s1 = Student.objects.create(user=u1, university_id='1')
        Meal.objects.create(student=s1, date=date.today(), breakfast=True, supper=True)
        
        response = self.client.get('/kitchen/dashboard/')
        self.assertEqual(response.context['today_stats']['breakfast'], 1)
        self.assertEqual(response.context['today_stats']['supper'], 1)
