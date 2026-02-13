from django.contrib import admin
from .models import StudentProfile

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'user', 'branch', 'cgpa', 'is_placed', 'highest_package')
    list_filter = ('branch', 'is_placed', 'year')
    search_fields = ('roll_number', 'user__username', 'user__email')
    readonly_fields = ('is_placed', 'highest_package')

admin.site.register(StudentProfile, StudentProfileAdmin)
