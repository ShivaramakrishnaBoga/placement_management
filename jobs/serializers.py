from rest_framework import serializers
from .models import JobDrive, Application, Offer, ApplicationField, ApplicationResponse
from students.serializers import StudentProfileSerializer
from django.utils import timezone

class ApplicationFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationField
        fields = ['id', 'field_name', 'field_type']

class JobDriveSerializer(serializers.ModelSerializer):
    fields = ApplicationFieldSerializer(many=True, read_only=True)
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = JobDrive
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'status']

class ApplicationSerializer(serializers.ModelSerializer):
    job_details = JobDriveSerializer(source='job', read_only=True)
    student_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['applied_at', 'status', 'viewed']

    def get_student_details(self, obj):
        # We need to fetch student profile
        try:
            return StudentProfileSerializer(obj.student.student_profile).data
        except:
            return None

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
