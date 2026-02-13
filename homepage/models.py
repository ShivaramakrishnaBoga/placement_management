from django.db import models

# Landing Page Control
class LandingPageSettings(models.Model):
    hero_background = models.ImageField(upload_to='hero/', blank=True, null=True)
    is_published = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Landing Page Settings"

# Scrolling Banner Announcements
class Announcement(models.Model):
    message = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
# Placed Student Success Stories
class SuccessStory(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    package = models.CharField(max_length=100)
    graduation_year = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='students/')
    testimonial = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.company}"

# testimonies
    class Testimonial(models.Model):
        name = models.CharField(max_length=200)
        role = models.CharField(max_length=200, blank=True, null=True)
        message = models.TextField()
        photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
        is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Dynamic Homepage Sections
class HomepageSection(models.Model):
    SECTION_CHOICES = (
        ('hero', 'Hero Section'),
        ('banner', 'Scrolling Banner'),
        ('success', 'Success Stories'),
        ('features', 'Features'),
        ('stats', 'Statistics'),
        ('testimonials', 'Testimonials'),
    )

    section_name = models.CharField(max_length=50, choices=SECTION_CHOICES)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.section_name

class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
