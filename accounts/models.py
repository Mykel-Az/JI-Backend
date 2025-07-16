from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.core.mail import send_mail
from core.common.models import *
from django.utils import timezone
from django.db.models import TextChoices


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    

class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_dormant=False, is_deleted=False)


class AccountType(TextChoices):
    COMPANY = 'company', 'Company'
    PROFESSIONAL = 'professional', 'Professional'
    TRADE_BUSINESS = 'trade_business', 'Trade Service Business'


class CustomUser(AbstractBaseUser, PermissionsMixin, SoftDeleteModel):
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_dormant = models.BooleanField(default=False)  # For soft deletion
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager() #all user
    active_user = ActiveUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["account_type"]),
            models.Index(fields=["is_active"]),
        ]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]
    
    @property
    def full_name(self):
        return self.get_full_name()
        
    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}".strip()







    

