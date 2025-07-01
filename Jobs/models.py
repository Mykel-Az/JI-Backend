from django.db import models
from cities_light.models import Country, City

# Create your models here.
class Location(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.city.name}, {self.country.name} - {self.address}"

class TimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 

class JobIndustry(TimeModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

class JobCategories(TimeModel):
    name = models.CharField(max_length=50)
    industry = models.ManyToManyField(JobIndustry)

class SubCategory(TimeModel):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(JobCategories)

class EmploymentType(TimeModel):
    name = models.CharField(max_length=50)
    duration = models.DurationField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_flexible = models.BooleanField(default=False)

class payment(TimeModel):
    name = models.CharField(max_length=50)
    currency = models.CharField(max_length=10, default='USD')
    bugdet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_flexible = models.BooleanField(default=False)

class JobTags(TimeModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class JobPost(TimeModel):
    JOB_TYPE_CHOICES = [
        ('remote', 'Remote'),
        ('onsite', 'Onsite'),
        ('hybrid', 'Hybrid'),
    ]

    job_id = models.UUIDField(primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES)
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.CASCADE)
    categories = models.ManyToManyField(JobCategories)
    payment = models.ForeignKey(payment, on_delete=models.CASCADE)
    full_details = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title



