from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name')
    search_fields = ('user__email', 'company_name')

admin.register(CompanyFAQ)
class CompanyFaqAdmin(admin.ModelAdmin):
    list_display = ('question')
    search_fields = ('question')

admin.register(CompanyTeamMember)
class CompanyTeammemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    search_fields = ('name', 'position')



