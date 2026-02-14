from django.db import models
from django.conf import settings
from jobs.models import JobDrive

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=255)
    details = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.action} - {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class PlacementPolicy(models.Model):
    """
    Global placement policies (Singleton pattern via logic or just one instance)
    """
    active_year = models.IntegerField(default=2024, unique=True)
    
    # Eligibility Defaults
    min_cgpa_default = models.DecimalField(max_digits=4, decimal_places=2, default=6.0)
    max_backlogs_allowed = models.IntegerField(default=1)

    # Offer Policies
    dream_offer_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=5.00, help_text="LPA")
    super_dream_offer_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=10.00, help_text="LPA")
    max_offers_per_student = models.IntegerField(default=1) # 1 offer usually, unless upgraded
    allow_dream_after_normal = models.BooleanField(default=True)
    allow_super_dream_after_dream = models.BooleanField(default=True)
    
    freeze_placement_season = models.BooleanField(default=False, help_text="If user checked, all applications are frozen")

    class Meta:
        verbose_name_plural = "Placement Policies"

    def __str__(self):
        return f"Policy for Year {self.active_year}"

class GuidanceContent(models.Model):
    RESOURCE_TYPES = [
        ("LINK", "Link"),
        ("PDF", "PDF"),
        ("VIDEO", "Video"),
        ("TEXT", "Text"),
    ]

    job = models.ForeignKey(JobDrive, on_delete=models.CASCADE)
    round_name = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to="guidance_files/", null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class StudentRoundStatus(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CLEARED", "Cleared"),
        ("FAILED", "Failed"),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(JobDrive, on_delete=models.CASCADE)
    round_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    updated_at = models.DateTimeField(auto_now=True)

