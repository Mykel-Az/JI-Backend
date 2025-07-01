from django.contrib.auth.models import AbstractUser
from django.db import models
from cities_light.models import Country, City

# Create your models here.
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    is_employer = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username