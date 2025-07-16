from django.db import models
from cities_light.models import Country, City
# from accounts.models import CustomUser
from geopy.geocoders import Nominatim
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator



class TimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Avoid creating a separate table


class Location(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.city.name}, {self.country.name} - {self.address}"
    
    def save(self, *args, **kwargs):
        full_address = f"{self.address}, {self.city.name}, {self.country.name}"

        if settings.ENABLE_GEOLOCATION:
            if not self.latitude or not self.longitude:
                try:
                    geolocator = Nominatim(user_agent="locator")
                    location = geolocator.geocode(full_address)
                    if location:
                        self.latitude = location.latitude
                        self.longitude = location.longitude
                except Exception as e:
                    print(f"[Geolocation Disabled] Error: {e}")
                    raise ValidationError(f"Geocoding error: {e}")
        
        super().save(*args, **kwargs)
        
        # Move geocoding to a Celery task if you're planning async job queueing later.
        # disable geocoding during tests or migrations.


class Review(TimeModel):
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.reviewer.email} for {self.reviewed_user.email} - Rating: {self.rating}"


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # to access all including deleted

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True



