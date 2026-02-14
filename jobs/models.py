from django.db import models
from django.conf import settings
from django.utils import timezone

class JobDrive(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('UPCOMING', 'Upcoming'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    ]

    CATEGORY_CHOICES = (
        ('NORMAL', 'Normal'),
        ('DREAM', 'Dream'),
        ('SUPER_DREAM', 'Super Dream'),
    )

    BRANCH_CHOICES = (
        ('CSE', 'CSE'),
        ('ECE', 'ECE'),
        ('EEE', 'EEE'),
        ('MECH', 'MECH'),
        ('CIVIL', 'CIVIL'),
        ('IT', 'IT'),
    )

    # Basic Info
    company_name = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Eligibility Criteria
    min_cgpa = models.FloatField(blank=True, null=True)
    max_backlogs = models.IntegerField(blank=True, null=True)
    cgpa_required = models.BooleanField(default=False)
    backlogs_required = models.BooleanField(default=False)
    eligible_branches = models.CharField(max_length=500, help_text="Comma-separated branches e.g. CSE,ECE", default="All")

    # Other eligibility
    eligible_batches = models.CharField(max_length=200, help_text="Comma-separated years (e.g., 2024,2025)", default="2024")

    # Offer Details
    ctc = models.DecimalField(max_digits=10, decimal_places=2, help_text="CTC in LPA")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='NORMAL')
    
    # Meta
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'OFFICER'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    
    # Optional Visuals
    image = models.ImageField(upload_to='job_images/', blank=True, null=True)
    card_color = models.CharField(max_length=20, default="#FFE4D6", blank=True, null=True)
    
    # Location
    location_city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.title}"

    @property
    def is_active(self):
        return self.status == 'OPEN' and (not self.application_deadline or self.application_deadline > timezone.now())


# Dynamic Application Fields (Keep existing logic)
class ApplicationField(models.Model):
    job = models.ForeignKey(JobDrive, on_delete=models.CASCADE, related_name='fields')
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50)  # text, number, file

    def __str__(self):
        return f"{self.job.title} - {self.field_name}"


class Application(models.Model):
    STATUS_CHOICES = (
        ('APPLIED', 'Applied'),
        ('SHORTLISTED', 'Shortlisted'),
        ('SELECTED', 'Selected'),
        ('REJECTED', 'Rejected'),   
    )

    job = models.ForeignKey(JobDrive, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    current_round = models.CharField(max_length=100, blank=True, default="Screening")

    viewed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('job', 'student')

class ApplicationResponse(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='responses')
    field = models.ForeignKey(ApplicationField, on_delete=models.CASCADE)
    value = models.TextField()

class Offer(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='offer')
    ctc_offered = models.DecimalField(max_digits=10, decimal_places=2)
    offer_letter = models.FileField(upload_to='offers/', null=True, blank=True)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
