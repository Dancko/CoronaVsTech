from django.db import models
from django.utils.timezone import now


class Company(models.Model):
    class CompanyStatus(models.TextChoices):
        LAYOFFS = "Layoffs"
        HIRING = "Hiring"
        HIRING_FREEZE = "Hiring Freeze"

    name = models.CharField(max_length=100, unique=True)
    company_status = models.CharField(
        max_length=13, choices=CompanyStatus.choices, default=CompanyStatus.HIRING
    )
    last_update = models.DateTimeField(default=now, editable=True)
    link = models.URLField(max_length=100, blank=True)
    note = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return str(self.name)
