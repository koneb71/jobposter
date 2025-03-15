from django import forms
from .models import JobListing, JobApplication

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title', 'company', 'location', 'description', 'requirements', 
                  'employment_type', 'salary_range', 'deadline', 'company_logo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'cover_letter', 'resume', 
                  'portfolio_url', 'linkedin_url']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us why you\'re a good fit for this position...'}),
            'portfolio_url': forms.URLInput(attrs={'placeholder': 'https://yourportfolio.com'}),
            'linkedin_url': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/yourprofile'}),
        } 