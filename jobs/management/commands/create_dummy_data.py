from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from jobs.models import JobListing, JobApplication, UserProfile
from faker import Faker
import random
from datetime import timedelta

fake = Faker()

class Command(BaseCommand):
    help = 'Creates dummy data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy data...')

        # Company logo services
        logo_services = [
            lambda company: f"https://logo.clearbit.com/{company.lower().replace(' ', '')}.com",
            lambda company: f"https://ui-avatars.com/api/?name={company.replace(' ', '+')}&background=random&size=128",
            lambda company: f"https://placehold.co/200x200/random/white?text={company.replace(' ', '+')}"
        ]

        # Create employers
        employers = []
        for _ in range(5):
            username = fake.user_name()
            while User.objects.filter(username=username).exists():
                username = fake.user_name()
            
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='testpass123'
            )
            
            # Generate company name and logo URL
            company_name = fake.company()
            logo_service = random.choice(logo_services)
            company_logo = logo_service(company_name)
            
            # Create employer profile
            profile = UserProfile.objects.create(
                user=user,
                company_name=company_name,
                company_logo=company_logo,
                company_description=fake.text(max_nb_chars=500),
                company_website=fake.url(),
                company_location=fake.city()
            )
            employers.append(user)
            self.stdout.write(f'Created employer: {username} ({company_name})')

        # Create job seekers
        job_seekers = []
        for _ in range(13):
            username = fake.user_name()
            while User.objects.filter(username=username).exists():
                username = fake.user_name()
            
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='testpass123'
            )
            
            # Create basic profile for job seeker
            profile = UserProfile.objects.create(
                user=user
            )
            job_seekers.append(user)
            self.stdout.write(f'Created job seeker: {username}')

        # Job titles for more realistic data
        job_titles = [
            'Software Engineer', 'Product Manager', 'Data Scientist', 
            'UX Designer', 'Marketing Manager', 'Sales Representative',
            'HR Manager', 'Financial Analyst', 'Business Development Manager',
            'Content Writer', 'DevOps Engineer', 'Project Manager',
            'Account Executive', 'Customer Success Manager', 'Research Analyst'
        ]

        # Salary ranges by job level
        salary_ranges = {
            'entry': {'min': 40000, 'max': 70000},
            'mid': {'min': 65000, 'max': 120000},
            'senior': {'min': 100000, 'max': 200000},
            'executive': {'min': 150000, 'max': 300000}
        }

        # Create job listings
        job_listings = []
        for employer in employers:
            # Each employer creates 2-4 jobs
            for _ in range(random.randint(2, 4)):
                # Select random job level and corresponding salary range
                job_level = random.choice(['entry', 'mid', 'senior', 'executive'])
                salary_range = salary_ranges[job_level]
                
                # Generate realistic salary within the range
                salary_min = round(random.uniform(salary_range['min'], salary_range['max'] * 0.7), -3)
                salary_max = round(random.uniform(salary_min * 1.1, salary_range['max']), -3)
                
                job = JobListing.objects.create(
                    user=employer,
                    title=random.choice(job_titles),
                    location=fake.city(),
                    description=fake.text(max_nb_chars=1000),
                    requirements='\n'.join([f'- {fake.sentence()}' for _ in range(5)]),
                    employment_type=random.choice([t[0] for t in JobListing.EMPLOYMENT_TYPES]),
                    salary_min=salary_min,
                    salary_max=salary_max,
                    salary_currency=random.choice([c[0] for c in JobListing.CURRENCY_CHOICES]),
                    deadline=timezone.now() + timedelta(days=random.randint(7, 60)),
                    is_active=True
                )
                job_listings.append(job)
                self.stdout.write(f'Created job listing: {job.title}')

        # Create job applications
        for job_seeker in job_seekers:
            # Each job seeker applies to 2-5 random jobs
            for job in random.sample(job_listings, random.randint(2, 5)):
                application = JobApplication.objects.create(
                    job=job,
                    full_name=fake.name(),
                    email=job_seeker.email,
                    phone=f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    cover_letter=fake.text(max_nb_chars=500),
                    status=random.choice([s[0] for s in JobApplication.STATUS_CHOICES]),
                    portfolio_url=fake.url() if random.choice([True, False]) else None,
                    linkedin_url=f"https://linkedin.com/in/{fake.user_name()}" if random.choice([True, False]) else None,
                    applied_date=timezone.now() - timedelta(days=random.randint(0, 30))
                )
                self.stdout.write(f'Created application: {application.full_name} for {job.title}')

        self.stdout.write(self.style.SUCCESS('Successfully created dummy data!')) 