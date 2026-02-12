from django.db import models
from django.conf import settings

class Job(models.Model):

    # Basic Info
    company_name = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    branches = models.CharField(max_length=200)

    # Optional Visuals
    image = models.ImageField(upload_to='job_images/', blank=True, null=True)
    card_color = models.CharField(max_length=20, default="#FFE4D6", blank=True, null=True)

    # Compensation
    salary_amount = models.IntegerField(blank=True, null=True)
    salary_period = models.CharField(max_length=20, blank=True, null=True)

    # Location
    location_city = models.CharField(max_length=100, blank=True, null=True)
    location_state = models.CharField(max_length=100, blank=True, null=True)

    # Tags
    job_tags = models.CharField(max_length=300, blank=True, null=True)

    # Meta
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        return self.job_tags.split(',') if self.job_tags else []



#Dynamic Field Model
class ApplicationField(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='fields')
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50)  # text, number, file

    def __str__(self):
        return f"{self.job.title} - {self.field_name}"


#Application Model
class Application(models.Model):

    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),   
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')

    class Meta:
        unique_together = ('job', 'student')


#dynamic responses
class ApplicationResponse(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='responses')
    field = models.ForeignKey(ApplicationField, on_delete=models.CASCADE)
    value = models.TextField()


class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]
