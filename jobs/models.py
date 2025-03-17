from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company_name = models.CharField(max_length=200, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_description = models.TextField(blank=True)
    company_website = models.URLField(blank=True)
    company_location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class JobListing(models.Model):
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('CAD', 'Canadian Dollar'),
        ('AUD', 'Australian Dollar'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_listings')
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    deadline = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def company(self):
        return self.user.profile.company_name

    @property
    def company_logo(self):
        return self.user.profile.company_logo

    @property
    def salary_range(self):
        return f"{self.salary_currency} {self.salary_min:,.2f} - {self.salary_max:,.2f}"

    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-created_at']

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('REVIEWED', 'Reviewed'),
        ('INTERVIEWED', 'Interviewed'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    portfolio_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    applied_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Application by {self.full_name} for {self.job.title}"
