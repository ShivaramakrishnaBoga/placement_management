from django.contrib import admin
from .models import (
    LandingPageSettings,
    Announcement,
    SuccessStory,
    Testimonial,
    HomepageSection
)

admin.site.register(LandingPageSettings)
admin.site.register(Announcement)
admin.site.register(SuccessStory)
admin.site.register(Testimonial)
admin.site.register(HomepageSection)
