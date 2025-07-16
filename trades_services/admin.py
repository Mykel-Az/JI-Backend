from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(TradeServiceProfile)
class TradeServiceProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__email',)