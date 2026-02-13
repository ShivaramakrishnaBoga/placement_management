from django.shortcuts import render
from .models import (
    LandingPageSettings,
    Announcement,
    SuccessStory,
    Testimonial,
    HomepageSection
)

def landing(request):

    settings = LandingPageSettings.objects.first()
    announcements = Announcement.objects.filter(is_active=True)
    stories = SuccessStory.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    sections = HomepageSection.objects.all()

    return render(request, 'landing.html', {
        'settings': settings,
        'announcements': announcements,
        'stories': stories,
        'testimonials': testimonials,
        'sections': sections
    })
