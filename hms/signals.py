from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from allauth.socialaccount.signals import pre_social_login
from .models import Student, LoginActivity, AuditLog
from .middleware import get_current_user
import json

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

# ============================================
# SECURITY & AUDIT LOGGING
# ============================================

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log user login activity"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    LoginActivity.objects.create(
        user=user,
        ip_address=ip,
        user_agent=user_agent
    )

@receiver(post_save)
@receiver(post_delete)
def log_audit_change(sender, instance, **kwargs):
    """Log changes to sensitive models"""
    # Ignore logging models and migration history
    if sender in [LoginActivity, AuditLog] or sender._meta.model_name == 'session' or sender._meta.app_label == 'admin':
        return
        
    user = get_current_user()
    if not user or not user.is_authenticated:
        return # Only log authenticated actions or rely on system (can create system user if needed)
    
    # Determine action
    if 'created' not in kwargs:
        action = 'DELETE'
    elif kwargs.get('created'):
        action = 'CREATE'
    else:
        action = 'UPDATE'
        
    object_repr = str(instance)[:200]
    object_id = str(instance.pk)
    model_name = sender.__name__
    
    AuditLog.objects.create(
        user=user,
        model_name=model_name,
        object_id=object_id,
        object_repr=object_repr,
        action=action,
        changes=f"{action} on {model_name}"
    )
