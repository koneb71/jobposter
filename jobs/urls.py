from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('jobs/', views.JobListView.as_view(), name='job-listings'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('job/new/', views.JobCreateView.as_view(), name='job-create'),
    path('job/<int:pk>/edit/', views.JobUpdateView.as_view(), name='job-update'),
    path('job/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job-delete'),
    path('job/<int:pk>/apply/', views.apply_for_job, name='job-apply'),
    path('job/<int:job_pk>/application/<int:application_pk>/review/', views.review_application, name='application-review'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
] 