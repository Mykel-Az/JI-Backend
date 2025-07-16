from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from accounts.models import *
from professionals.models import ProfessionalUserProfile
from Jobs.models import *
from core.common.models import TimeModel


def validate_year(value):
    if value > date.today().year:
        raise ValidationError("Founded year cannot be in the future.")


class CompanyTeamMember(TimeModel):

    position_choice = [
        ('founder', 'Founder'),
        ('director', 'Director'),
        ('executive', 'Executive'),
    ]

    name = models.ForeignKey('professionals.ProfessionalUserProfile', on_delete=models.CASCADE, related_name='team_members')
    postion = models.CharField(max_length=50, choices=position_choice, null=True, blank=True)

    def __str__(self):
        return f"{self.name.get_full_name()} ({self.postion})"


class CompanyFAQ(TimeModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"{self.question}"


class CompanyProfile(TimeModel):

    company_size_choices = [
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1000+', '1000+ employees'),
    ]
    
    # Account owner
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile', verbose_name="Account Owner")
    # Company identity
    company_name = models.CharField(max_length=255, unique=True, verbose_name="Company Name", help_text="The official name of your company")
    slug = models.SlugField(unique=True, blank=True)
    industry = models.ForeignKey(JobIndustry, on_delete=models.PROTECT, verbose_name="Primary Industry")
    category = models.ForeignKey(JobCategory, on_delete=models.PROTECT, verbose_name="Business Category", default=None, null=True, blank=True)
    company_size = models.CharField(max_length=50, blank=True, null=True, choices=company_size_choices, verbose_name="Company Size")
    founded_year = models.PositiveIntegerField(blank=True, null=True, validators=[validate_year], verbose_name="Year Founded")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Headquarters Location")
    is_remote_friendly = models.BooleanField(default=False, verbose_name="Remote-Friendly Company" )
    # Branding & Description
    tagline = models.CharField(max_length=150, blank=True, null=True, verbose_name="Company Tagline", help_text="A short, catchy phrase about your company")
    description = models.TextField(blank=True, null=True, verbose_name="Company Description", help_text="Detailed information about your company")
    mission_statement = models.TextField(blank=True, null=True, verbose_name="Mission Statement")
    # Media & social links
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="Company Logo", help_text="Upload your company logo (optimal size: 400x400px)")
    cover_image = models.ImageField(upload_to='company_covers/', blank=True, null=True, verbose_name="Cover Image", help_text="Upload a cover image for your company profile (optimal size: 1500x500px)")
    website = models.URLField(blank=True, null=True, validators=[URLValidator()], verbose_name="Company Website")
    linkedin_url = models.URLField(blank=True, null=True, verbose_name="LinkedIn Profile")
    twitter_url = models.URLField(blank=True, null=True, verbose_name="Twitter Profile")
    # alumini and know more
    Alumini = models.ForeignKey(CompanyTeamMember, on_delete=models.CASCADE, related_name='company_members', null=True, blank=True)
    faqs = models.ForeignKey(CompanyFAQ, on_delete=models.PROTECT, related_name='companyfaq', null=True, blank=True, verbose_name="FAQs")
    # Contact
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Contact Email")
    contact_phone = PhoneNumberField( blank=True, null=True, verbose_name="Contact Phone")
    # Social features
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='following_companies', verbose_name="Followers")
    reviews = models.ManyToManyField(Review, blank=True, related_name='companies', verbose_name="Company Reviews")
    # Status
    is_verified = models.BooleanField(default=False, verbose_name="Verified Company")
    is_active = models.BooleanField(default=True, verbose_name="Active Profile")

    

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profiles"
        ordering = ['company_name']

    def __str__(self):
        return self.company_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.company_name)
        super().save(*args, **kwargs)

    @property
    def total_jobs_posted(self):
        return self.jobs.count()  # related_name from Job model
    
    def total_jobs_open(self):
        return self.jobs.filter(job_status='open').count()

    @property
    def total_followers(self):
        return self.followers.count()

    @property
    def average_rating(self):
        if self.reviews.exists():
            return self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        return None



# class CompanySubscription(TimeModel):
#     company = models.OneToOneField('CompanyProfile', on_delete=models.CASCADE)
#     plan_name = models.CharField(max_length=100)
#     features = models.TextField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.company.company_name} - {self.plan_name}"
