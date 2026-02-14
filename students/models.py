from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentProfile(models.Model):
    BRANCH_CHOICES = (
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics and Communication'),
        ('EEE', 'Electrical and Electronics'),
        ('MECH', 'Mechanical'),
        ('CIVIL', 'Civil'),
        ('IT', 'Information Technology'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=100, choices=BRANCH_CHOICES)
    year = models.IntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)])
    
    # Academic Data (Read-Only for Students, Writable by Admin)
    cgpa = models.FloatField(default=0.0)
    backlogs = models.IntegerField(default=0)
    
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    academic_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Resume
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    
    # Placement Stats
    is_placed = models.BooleanField(default=False)
    highest_package = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="In LPA")
    
    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name()}"
