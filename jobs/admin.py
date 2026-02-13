from django.contrib import admin
from .models import JobDrive, ApplicationField, Application, ApplicationResponse, Offer

class ApplicationFieldInline(admin.TabularInline):
    model = ApplicationField
    extra = 1

class JobDriveAdmin(admin.ModelAdmin):
    inlines = [ApplicationFieldInline]
    list_display = ('title', 'company_name', 'status', 'created_at')
    list_filter = ('status', 'company_name')

admin.site.register(JobDrive, JobDriveAdmin)
admin.site.register(Application)
admin.site.register(ApplicationResponse)
admin.site.register(Offer)