from django.contrib import admin
from .models import Job, ApplicationField, Application, ApplicationResponse
from .models import Notification

admin.site.register(Job)
admin.site.register(ApplicationField)
admin.site.register(Application)
admin.site.register(ApplicationResponse)
admin.site.register(Notification)