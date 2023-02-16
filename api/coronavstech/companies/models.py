from django.db import models


class Company(models.Model):
    class CompanyStatus(models.TextChoices):
        LAYOFFS = 'Layoffs'
        HIRING = 'Hiring'
        HIRING_FREEZE = 'Hiring Freeze'

    name = models.CharField(max_length=100, unique=True)
    company_status = models.CharField(max_length=13, choices=CompanyStatus.choices, default=CompanyStatus.HIRING)
    last_update = models.DateTimeField(auto_now_add=True, editable=True)
    link = models.URLField(blank=True)
    note = models.CharField(max_length=150, blank=True)
