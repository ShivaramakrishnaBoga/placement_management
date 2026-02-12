from django.contrib.auth.models import AbstractUser
from django.db import models


#CUSTOM USER MODEL
class User(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('OFFICER', 'Placement Officer'),
        ('STUDENT', 'Student'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')


    roll_number = models.CharField(max_length=20, blank=True, null=True)
    branch = models.CharField(max_length=50, blank=True, null=True)
    cgpa = models.FloatField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username
