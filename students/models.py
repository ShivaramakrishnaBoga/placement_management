from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=100)  # Make this a ChoiceField if possible, but CharField for flexibility for now
    year = models.IntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)])
    
    # Academic Data (Read-Only for Students, Writable by Admin)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    active_backlogs = models.IntegerField(default=0)
    history_backlogs = models.IntegerField(default=0)
    
    academic_verified = models.BooleanField(default=False)
    
    # Resume
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    
    # Placement Stats
    is_placed = models.BooleanField(default=False)
    highest_package = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="In LPA")
    
    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name()}"
