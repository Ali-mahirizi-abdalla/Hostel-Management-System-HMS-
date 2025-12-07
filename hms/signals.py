from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.socialaccount.signals import pre_social_login
from .models import StudentProfile


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """Create StudentProfile for new users"""
    if created and not hasattr(instance, 'student_profile'):
        StudentProfile.objects.create(
            user=instance,
            room_number='TBD',  # To be determined - user can update later
            phone_number=''
        )


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    """
    Link social account to existing user if email matches
    """
    email = sociallogin.account.extra_data.get('email')
    if email:
        try:
            user = User.objects.get(email=email)
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass
