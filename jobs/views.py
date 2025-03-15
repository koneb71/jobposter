from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods

from .models import JobListing, JobApplication
from .forms import JobListingForm, JobApplicationForm

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

class JobCreateView(LoginRequiredMixin, CreateView):
    model = JobListing
    form_class = JobListingForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Job listing created successfully!')
        return super().form_valid(form)

class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = JobListing
    form_class = JobListingForm
    template_name = 'jobs/job_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Job listing updated successfully!')
        return super().form_valid(form)

class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = JobListing
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('home')
    
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

@require_http_methods(["GET", "POST"])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('home')
    return render(request, 'jobs/logout.html')
