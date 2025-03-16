from django.contrib import admin
from .models import JobListing, JobApplication, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_location', 'created_at')
    search_fields = ('user__username', 'company_name', 'company_location')
    list_filter = ('created_at',)

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'location', 'employment_type', 'created_at', 'is_active')
    list_filter = ('employment_type', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'created_at'

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'job', 'status', 'applied_date')
    list_filter = ('status', 'applied_date')
    search_fields = ('full_name', 'email', 'job__title')
    date_hierarchy = 'applied_date'
    readonly_fields = ('applied_date',)
    fieldsets = (
        ('Applicant Information', {
            'fields': ('full_name', 'email', 'phone', 'cover_letter')
        }),
        ('Job Information', {
            'fields': ('job', 'status', 'applied_date')
        }),
        ('Professional Links', {
            'fields': ('portfolio_url', 'linkedin_url'),
            'classes': ('collapse',)
        }),
        ('Resume', {
            'fields': ('resume',),
            'description': 'View the applicant\'s uploaded resume'
        })
    )
    ordering = ('-applied_date',)
    actions = ['mark_as_reviewed', 'mark_as_interviewed', 'mark_as_accepted', 'mark_as_rejected']

    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='REVIEWED')
    mark_as_reviewed.short_description = "Mark selected applications as reviewed"

    def mark_as_interviewed(self, request, queryset):
        queryset.update(status='INTERVIEWED')
    mark_as_interviewed.short_description = "Mark selected applications as interviewed"

    def mark_as_accepted(self, request, queryset):
        queryset.update(status='ACCEPTED')
    mark_as_accepted.short_description = "Mark selected applications as accepted"

    def mark_as_rejected(self, request, queryset):
        queryset.update(status='REJECTED')
    mark_as_rejected.short_description = "Mark selected applications as rejected"
