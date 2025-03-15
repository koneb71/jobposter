from django.db import models
from django.utils import timezone
from django.urls import reverse

class JobListing(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('FULL_TIME', 'Full-time'),
        ('PART_TIME', 'Part-time'),
        ('CONTRACT', 'Contract'),
        ('INTERNSHIP', 'Internship'),
        ('REMOTE', 'Remote'),
    ]
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='FULL_TIME')
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    posted_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-posted_date']

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
