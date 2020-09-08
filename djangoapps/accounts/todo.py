# main/models.py
#https://code.tutsplus.com/ru/tutorials/using-celery-with-django-for-background-task-processing--cms-28732

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
 
 
class UserAccountManager(BaseUserManager):
    use_in_migrations = True
 
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')
 
        if not password:
            raise ValueError('Password must be provided')
 
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)
 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
 
        return self._create_user(email, password, **extra_fields)
 
 
class User(AbstractBaseUser, PermissionsMixin):
 
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
 
    objects = UserAccountManager()
 
    email = models.EmailField('email', unique=True, blank=False, null=False)
    full_name = models.CharField('full name', blank=True, null=True, max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
 
    def get_short_name(self):
        return self.email
 
    def get_full_name(self):
        return self.email
 
    def __unicode__(self):
        return self.email

AUTH_USER_MODEL = 'main.User'

from django.db.models import signals
from django.core.mail import send_mail
 
 
def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        # Send verification email
        send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
                'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(instance.verification_uuid)}),
            'from@quickpublisher.dev',
            [instance.email],
            fail_silently=False,
        )
 
signals.post_save.connect(user_post_save, sender=User)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '<YOUR_GMAIL_USERNAME>@gmail.com'
EMAIL_HOST_PASSWORD = '<YOUR_GMAIL_PASSWORD>'
EMAIL_PORT = 587



# main/views.py
 
from django.http import Http404
from django.shortcuts import render, redirect
from .models import User
 
 
def home(request):
    return render(request, 'home.html')
 
 
def verify(request, uuid):
    try:
        user = User.objects.get(verification_uuid=uuid, is_verified=False)
    except User.DoesNotExist:
        raise Http404("User does not exist or is already verified")
 
    user.is_verified = True
    user.save()
 
    return redirect('home')