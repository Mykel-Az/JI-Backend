from django.db import models
from accounts.models import *
from Jobs.models import TimeModel
from django.conf import settings

# Create your models here.

class TradeServiceProfile(TimeModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tradeserviceprofile')
    services_offered = models.TextField(help_text="Comma-separated list of services, e.g. Plumbing, Electrical")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    service_area_radius_km = models.PositiveIntegerField(default=20)  # for location matching
    available = models.BooleanField(default=True)
