from django.contrib import admin
from .models import (
    JobIndustry, JobCategory, EmploymentType, PaymentType, 
    Payment, JobTag, JobPost, JobApplication, SavedJob
)


@admin.register(JobIndustry)
class JobIndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'parent_category')
    search_fields = ('name', 'industry__name')
    list_filter = ('industry', 'parent_category')
    ordering = ('name',)


@admin.register(EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_flexible')
    search_fields = ('name',)
    list_filter = ('is_flexible',)
    ordering = ('name',)


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_type', 'currency', 'min_amount', 'max_amount', 'is_negotiable')
    search_fields = ('currency', 'payment_type__name')
    ordering = ('-min_amount',)


@admin.register(JobTag)
class JobTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_featured')
    search_fields = ('name',)
    list_filter = ('is_featured',)
    ordering = ('name',)


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'employment_type', 'created_at', 'is_active', 'is_featured')
    search_fields = ('title', 'company__company_name')
    list_filter = ('employment_type', 'location', 'is_active', 'is_featured', 'experience_level', 'work_model')
    ordering = ('-created_at',)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'status_changed_at')
    search_fields = ('job__title', 'applicant__email')
    list_filter = ('status', 'status_changed_at')
    ordering = ('-status_changed_at',)


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job',)
    search_fields = ('job__title', 'user__email')
    ordering = ('-created_at',)
