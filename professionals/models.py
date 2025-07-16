from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from Jobs.models import TimeModel, JobType, JobCategory
from core.common.models import SoftDeleteModel, Location


class Skill(TimeModel, SoftDeleteModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="Skill Name", help_text="Name of the skill (e.g., Python, Project Management)" )
    category = models.CharField(max_length=50, blank=True, null=True, verbose_name="Skill Category",  help_text="General category this skill belongs to")

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ['name']

    def __str__(self):
        return self.name


class ProfessionalUserProfile(TimeModel):

    availability_status_choices = [
        ('actively_looking', 'Actively looking'),
        ('open_to_offers', 'Open to offers'),
        ('not_looking', 'Not currently looking'),
    ]

    # 🔹 User
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='professional_profile', verbose_name="User Account")
    # 🔹 Personal Info
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Profile Picture")
    headline = models.CharField(max_length=120, blank=True, null=True, verbose_name="Professional Headline")
    bio = models.TextField(blank=True, null=True, verbose_name="Professional Summary")
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Contact Phone")
    website = models.URLField(blank=True, null=True, verbose_name="Personal Website / Portfolio")
    linkedin_profile = models.URLField(blank=True, null=True, verbose_name="LinkedIn Profile")
    github_profile = models.URLField(blank=True, null=True, verbose_name="GitHub Profile")
    # 🔹 Experience & Skills
    profession = models.CharField(max_length=100, blank=True, null=True, verbose_name="Primary Profession")
    current_employer = models.CharField(max_length=255, blank=True, null=True, verbose_name="Current Employer")
    experience_years = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(70)], verbose_name="Years of Experience")
    skills = models.ManyToManyField(Skill, blank=True, related_name='professionals', verbose_name="Skills & Competencies")
    work_experience = models.TextField(blank=True, null=True, verbose_name="Work Experience")
    education = models.CharField(max_length=255, blank=True, null=True, verbose_name="Highest Education")
    certifications = models.TextField(blank=True, null=True, verbose_name="Certifications")
    # 🔹 Location
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Current Location")
    is_willing_to_relocate = models.BooleanField(default=False, verbose_name="Willing to Relocate")
    is_remote_preferred = models.BooleanField(default=False, verbose_name="Prefers Remote Work")
    # 🔹 Job Preferences
    availability_status = models.CharField(max_length=50, choices=availability_status_choices, default='open_to_offers', verbose_name="Availability Status")
    desired_salary_range = models.CharField(max_length=50, blank=True, null=True, verbose_name="Desired Salary Range")
    job_type_interests = models.ManyToManyField(JobType, blank=True, related_name='interested_professionals', verbose_name="Preferred Job Types")
    job_role_interests = models.ManyToManyField(JobCategory,  blank=True, related_name='interested_professionals', verbose_name="Preferred Job Roles")
    job_interest_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='job_seekers', verbose_name="Preferred Job Location")
    job_search_preferences = models.TextField( blank=True, null=True, verbose_name="Job Search Preferences")
    # 🔹 Documents
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, verbose_name="Resume / CV")
    cover_letter_template = models.FileField(upload_to='cover_letters/', blank=True, null=True, verbose_name="Cover Letter Template")
    # 🔹 Status & Visibility
    is_verified = models.BooleanField(default=False, verbose_name="Verified Professional")
    is_profile_public = models.BooleanField(default=True, verbose_name="Public Profile")

    class Meta:
        verbose_name = "Professional Profile"
        verbose_name_plural = "Professional Profiles"
        ordering = ['user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()}'s Professional Profile" if self.user else "Unattached Profile"

    @property
    def full_name(self):
        return self.user.get_full_name() if self.user else ""

    @property
    def primary_skill_list(self):
        return self.skills.all()[:5]

    @property
    def experience_level(self):
        if self.experience_years >= 15:
            return "Senior Executive"
        elif self.experience_years >= 10:
            return "Senior"
        elif self.experience_years >= 5:
            return "Mid-Level"
        elif self.experience_years >= 2:
            return "Junior"
        else:
            return "Entry Level"
