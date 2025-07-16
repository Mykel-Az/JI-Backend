from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from core.common.models import TimeModel, SoftDeleteModel, Location
import uuid
from django.utils import timezone


class JobIndustry(TimeModel, SoftDeleteModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Industry Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Job Industry")
        verbose_name_plural = _("Job Industries")
        ordering = ['name']

    def __str__(self):
        return self.name


class JobCategory(TimeModel, SoftDeleteModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Category Name"))
    industry = models.ForeignKey(JobIndustry, on_delete=models.PROTECT, related_name='categories')
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')

    class Meta:
        verbose_name = _("Job Category")
        verbose_name_plural = _("Job Categories")
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'industry'], name='unique_category_per_industry')
        ]

    def __str__(self):
        return f"{self.name} ({self.industry})"


class EmploymentType(TimeModel, SoftDeleteModel):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', _("Full-time")),
        ('part_time', _("Part-time")),
        ('contract', _("Contract")),
        ('temporary', _("Temporary")),
        ('internship', _("Internship")),
        ('freelance', _("Freelance")),
    ]

    name = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    is_flexible = models.BooleanField(default=False, help_text=_("Supports flexible work hours"))

    class Meta:
        verbose_name = _("Employment Type")
        verbose_name_plural = _("Employment Types")
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class PaymentType(TimeModel, SoftDeleteModel):
    PAYMENT_TYPES_CHOICES = [
        ('salary', _("Salary")),
        ('hourly', _("Hourly")),
        ('project', _("Project-based")),
        ('contract', _("Contract")),
        ('stipend', _("Stipend")),
        ('commission', _("Commission")),
        ('equity', _("Equity")),
        ('bonus', _("Bonus")),
        ('other', _("Other")),
    ]

    name = models.CharField(max_length=20, choices=PAYMENT_TYPES_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Payment Type")
        verbose_name_plural = _("Payment Types")

    def __str__(self):
        return self.get_name_display()


class Payment(TimeModel):
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT , related_name='payments', default='salary')
    currency = models.CharField(max_length=10, default='USD')
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_negotiable = models.BooleanField(default=False)
    bonus_opportunities = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Payment Information")
        verbose_name_plural = _("Payment Information")

    def __str__(self):
        if self.min_amount and self.max_amount:
            return f"{self.currency} {self.min_amount}–{self.max_amount} ({self.payment_type})"
        elif self.min_amount:
            return f"{self.currency} {self.min_amount}+ ({self.payment_type})"
        return f"{self.payment_type} ({self.currency})"


class JobTag(TimeModel, SoftDeleteModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Job Tag")
        verbose_name_plural = _("Job Tags")
        ordering = ['name']

    def __str__(self):
        return self.name
    

class JobType(TimeModel, SoftDeleteModel):
    JOB_TYPE_CHOICES = [
        ('remote', _("Remote")),
        ('onsite', _("Onsite")),
        ('hybrid', _("Hybrid")),
    ]

    name = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Job Type")
        verbose_name_plural = _("Job Types")
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class JobPost(TimeModel):

    JOBS_STATUS_CHOICES = [ ( 'open', _("Open")), ('screening', _("screening")), ( 'closed', _("Closed") ),]    
    EXPERIENCE_LEVEL_CHOICES = [('entry', _("Entry")), ('mid', _("Mid")), ('senior', _("Senior")), ('executive', _("Executive"))]

    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    company = models.ForeignKey('company.CompanyProfile', on_delete=models.CASCADE, related_name='company_jobs')
    industry = models.ForeignKey(JobIndustry, on_delete=models.PROTECT, related_name='industry_jobs')
    category = models.ForeignKey(JobCategory, on_delete=models.PROTECT, related_name='category_jobs')
    description = models.TextField()
    requirements = models.TextField()
    JOB_STATUS = models.CharField(max_length=20, choices=JOBS_STATUS_CHOICES, default='open')
    benefits = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='job_locations')
    work_model = models.ForeignKey(JobType, on_delete=models.PROTECT, related_name='work_model_jobs')
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.PROTECT, related_name='employment_jobs')
    payment = models.OneToOneField(Payment, on_delete=models.PROTECT)
    tags = models.ManyToManyField(JobTag, blank=True, related_name='tagged_jobs')
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_LEVEL_CHOICES)
    application_deadline = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    applications_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Job Post")
        verbose_name_plural = _("Job Posts")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['industry']),
            models.Index(fields=['is_active']),
            models.Index(fields=['experience_level']),
        ]

    def __str__(self):
        return f"{self.title} @ {self.company.company_name}"

    @property
    def is_expired(self):
        return self.application_deadline and self.application_deadline < timezone.now().date()

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class JobApplication(TimeModel):
    APPLICATION_STATUS = [
        ('pending', _("Pending")),
        ('reviewed', _("Reviewed")),
        ('shortlisted', _("Shortlisted")),
        ('interviewing', _("Interviewing")),
        ('offer', _("Offer Extended")),
        ('hired', _("Hired")),
        ('rejected', _("Rejected")),
        ('withdrawn', _("Withdrawn")),
    ]

    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='applications/resumes/%Y/%m/%d/', blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='pending')
    status_changed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Job Application")
        verbose_name_plural = _("Job Applications")
        ordering = ['-created_at']
        unique_together = ['job', 'applicant']
        indexes = [models.Index(fields=['status']), models.Index(fields=['is_active'])]

    def __str__(self):
        return f"{self.applicant.get_full_name()} → {self.job.title}"

    def save(self, *args, **kwargs):
        if self.pk:
            original = JobApplication.objects.get(pk=self.pk)
            if original.status != self.status:
                self.status_changed_at = timezone.now()
        super().save(*args, **kwargs)


class SavedJob(TimeModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='savers')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Saved Job")
        verbose_name_plural = _("Saved Jobs")
        unique_together = ['user', 'job']

    def __str__(self):
        return f"{self.user} saved {self.job.title}"


# class TradeServiceJobPost(BaseJobPost):
#     service_area_radius_km = models.PositiveIntegerField(default=20)


# class JobApplication(TimeModel):
#     job = models.ForeignKey(ProfessionalJobPost, on_delete=models.CASCADE, related_name='applications')
#     applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     resume = models.FileField(upload_to='applications/resumes/', null=True, blank=True)
#     cover_letter = models.TextField(null=True, blank=True)
#     status = models.CharField(max_length=20, choices=[
#         ('pending', 'Pending'),
#         ('reviewed', 'Reviewed'),
#         ('interview', 'Interview Scheduled'),
#         ('rejected', 'Rejected'),
#         ('hired', 'Hired')
#     ], default='pending')

#     def __str__(self):
#         return f"{self.applicant.get_full_name()} - {self.job.title}"
