# Generated by Django 5.1.7 on 2025-03-17 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0003_alter_joblisting_options_remove_joblisting_company_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="joblisting",
            name="salary_range",
        ),
        migrations.AddField(
            model_name="joblisting",
            name="salary_currency",
            field=models.CharField(
                choices=[
                    ("USD", "US Dollar"),
                    ("EUR", "Euro"),
                    ("GBP", "British Pound"),
                    ("CAD", "Canadian Dollar"),
                    ("AUD", "Australian Dollar"),
                ],
                default="USD",
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="salary_max",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="salary_min",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
