from django.contrib import admin
from .models import JobListing, JobApplication

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'employment_type', 'posted_date', 'is_active')
    list_filter = ('is_active', 'employment_type', 'posted_date')
    search_fields = ('title', 'company', 'description')
    date_hierarchy = 'posted_date'

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'job', 'status', 'applied_date')
    list_filter = ('status', 'applied_date')
    search_fields = ('full_name', 'email', 'job__title')
    date_hierarchy = 'applied_date'
