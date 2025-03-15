from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('job/new/', views.JobCreateView.as_view(), name='job-create'),
    path('job/<int:pk>/update/', views.JobUpdateView.as_view(), name='job-update'),
    path('job/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job-delete'),
    path('job/<int:pk>/apply/', views.apply_for_job, name='job-apply'),
] 