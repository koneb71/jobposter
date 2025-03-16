from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Q, Count, Avg, F, ExpressionWrapper, fields, DurationField
from django.db.models.functions import ExtractDay, Cast
from django.contrib.auth import logout, login
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import json

from .models import JobListing, JobApplication, UserProfile
from .forms import JobListingForm, JobApplicationForm, UserRegistrationForm, UserProfileForm

class HomeView(ListView):
    model = JobListing
    template_name = 'jobs/home.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return JobListing.objects.filter(
                Q(title__icontains=query) | 
                Q(company__icontains=query) | 
                Q(location__icontains=query) |
                Q(description__icontains=query)
            ).filter(is_active=True)
        return JobListing.objects.filter(is_active=True)

class JobDetailView(DetailView):
    model = JobListing
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        context['applications'] = job.applications.all().order_by('-applied_date')
        context['is_job_owner'] = self.request.user.is_authenticated and job.user == self.request.user
        return context

class JobCreateView(LoginRequiredMixin, CreateView):
    model = JobListing
    form_class = JobListingForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Job listing created successfully!')
        return super().form_valid(form)

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobListing
    form_class = JobListingForm
    template_name = 'jobs/job_form.html'
    
    def test_func(self):
        job = self.get_object()
        return job.user == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Job listing updated successfully!')
        return super().form_valid(form)

class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JobListing
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        job = self.get_object()
        return job.user == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Job listing deleted successfully!')
        return super().delete(request, *args, **kwargs)

def apply_for_job(request, pk):
    job = get_object_or_404(JobListing, pk=pk)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job-detail', pk=job.pk)
    else:
        form = JobApplicationForm()
    
    return render(request, 'jobs/job_application_form.html', {'form': form, 'job': job})

def review_application(request, job_pk, application_pk):
    job = get_object_or_404(JobListing, pk=job_pk)
    application = get_object_or_404(JobApplication, pk=application_pk, job=job)
    
    # Check if the user is the job owner
    if not request.user.is_authenticated or job.user != request.user:
        return HttpResponseForbidden("You don't have permission to review this application.")
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}')
            return redirect('review-application', job_pk=job.pk, application_pk=application.pk)
    
    return render(request, 'jobs/application_review.html', {
        'job': job,
        'application': application,
    })

@require_http_methods(["GET", "POST"])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('home')
    return render(request, 'jobs/logout.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to JobPoster.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'jobs/register.html', {'form': form})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'jobs/profile.html', {
        'form': form,
        'profile': profile,
        'job_count': request.user.job_listings.count(),
        'application_count': JobApplication.objects.filter(job__user=request.user).count(),
    })

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Date ranges
        now = timezone.now()
        month_ago = now - timedelta(days=30)
        two_months_ago = now - timedelta(days=60)
        
        # Active Jobs Stats
        active_jobs = JobListing.objects.filter(user=user, is_active=True)
        active_jobs_count = active_jobs.count()
        active_jobs_last_month = JobListing.objects.filter(
            user=user,
            is_active=True,
            created_at__range=[month_ago, now]
        ).count()
        active_jobs_previous_month = JobListing.objects.filter(
            user=user,
            is_active=True,
            created_at__range=[two_months_ago, month_ago]
        ).count()
        
        # Calculate growth percentages
        active_jobs_growth = 0
        if active_jobs_previous_month > 0:
            active_jobs_growth = ((active_jobs_last_month - active_jobs_previous_month) / 
                                active_jobs_previous_month * 100)
        
        # Applications Stats
        total_applications = JobApplication.objects.filter(job__user=user).count()
        applications_last_month = JobApplication.objects.filter(
            job__user=user,
            applied_date__range=[month_ago, now]
        ).count()
        applications_previous_month = JobApplication.objects.filter(
            job__user=user,
            applied_date__range=[two_months_ago, month_ago]
        ).count()
        
        applications_growth = 0
        if applications_previous_month > 0:
            applications_growth = ((applications_last_month - applications_previous_month) / 
                                 applications_previous_month * 100)
        
        # Application Rate
        application_rate = 0
        if active_jobs_count > 0:
            application_rate = round(total_applications / active_jobs_count, 1)
        
        # Average Time to Fill
        filled_jobs = JobApplication.objects.filter(
            job__user=user,
            status='ACCEPTED'
        ).annotate(
            time_diff=ExpressionWrapper(
                F('applied_date') - F('job__created_at'),
                output_field=DurationField()
            )
        ).annotate(
            days_to_fill=ExtractDay('time_diff')
        )
        avg_time_to_fill = round(filled_jobs.aggregate(Avg('days_to_fill'))['days_to_fill__avg'] or 0)
        
        # Applications Timeline
        timeline_data = JobApplication.objects.filter(
            job__user=user,
            applied_date__gte=month_ago
        ).values('applied_date__date').annotate(
            count=Count('id')
        ).order_by('applied_date__date')
        
        applications_timeline_labels = [d['applied_date__date'].strftime('%Y-%m-%d') 
                                     for d in timeline_data]
        applications_timeline_data = [d['count'] for d in timeline_data]
        
        # Job Types Distribution
        job_types = JobListing.objects.filter(
            user=user
        ).values('employment_type').annotate(
            count=Count('id')
        )
        job_types_labels = [dict(JobListing.EMPLOYMENT_TYPES)[t['employment_type']] 
                          for t in job_types]
        job_types_data = [t['count'] for t in job_types]
        
        # Application Status Distribution
        status_dist = JobApplication.objects.filter(
            job__user=user
        ).values('status').annotate(
            count=Count('id')
        )
        status_labels = [dict(JobApplication.STATUS_CHOICES)[s['status']] 
                        for s in status_dist]
        status_data = [s['count'] for s in status_dist]
        
        # Top Locations
        top_locations = JobListing.objects.filter(
            user=user
        ).values('location').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        locations_labels = [l['location'] for l in top_locations]
        locations_data = [l['count'] for l in top_locations]
        
        context.update({
            'active_jobs_count': active_jobs_count,
            'active_jobs_growth': round(active_jobs_growth, 1),
            'total_applications': total_applications,
            'applications_growth': round(applications_growth, 1),
            'application_rate': application_rate,
            'avg_time_to_fill': avg_time_to_fill,
            'applications_timeline_labels': json.dumps(applications_timeline_labels),
            'applications_timeline_data': applications_timeline_data,
            'job_types_labels': json.dumps(job_types_labels),
            'job_types_data': job_types_data,
            'status_labels': json.dumps(status_labels),
            'status_data': status_data,
            'locations_labels': json.dumps(locations_labels),
            'locations_data': locations_data,
        })
        
        return context
