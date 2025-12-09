from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.socialaccount.signals import pre_social_login
from .models import Student


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """Create Student profile for new users"""
    if created and not hasattr(instance, 'student_profile'):
        Student.objects.create(
            user=instance,
            university_id=None, 
            phone=''
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
