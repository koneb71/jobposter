# Generated by Django 5.1.7 on 2025-03-15 14:34

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="JobListing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("company", models.CharField(max_length=200)),
                ("location", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("requirements", models.TextField()),
                (
                    "employment_type",
                    models.CharField(
                        choices=[
                            ("FULL_TIME", "Full-time"),
                            ("PART_TIME", "Part-time"),
                            ("CONTRACT", "Contract"),
                            ("INTERNSHIP", "Internship"),
                            ("REMOTE", "Remote"),
                        ],
                        default="FULL_TIME",
                        max_length=20,
                    ),
                ),
                (
                    "salary_range",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "posted_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deadline", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "company_logo",
                    models.ImageField(
                        blank=True, null=True, upload_to="company_logos/"
                    ),
                ),
            ],
            options={
                "ordering": ["-posted_date"],
            },
        ),
        migrations.CreateModel(
            name="JobApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("cover_letter", models.TextField()),
                ("resume", models.FileField(upload_to="resumes/")),
                ("portfolio_url", models.URLField(blank=True, null=True)),
                ("linkedin_url", models.URLField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("REVIEWED", "Reviewed"),
                            ("INTERVIEWED", "Interviewed"),
                            ("ACCEPTED", "Accepted"),
                            ("REJECTED", "Rejected"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                (
                    "applied_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications",
                        to="jobs.joblisting",
                    ),
                ),
            ],
        ),
    ]
