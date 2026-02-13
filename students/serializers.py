from rest_framework import serializers
from .models import StudentProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ['academic_verified', 'is_placed', 'highest_package']

class AcademicDataSerializer(serializers.ModelSerializer):
    # Specialized serializer for admin updates
    class Meta:
        model = StudentProfile
        fields = ['roll_number', 'cgpa', 'active_backlogs', 'history_backlogs', 'year', 'branch', 'academic_verified']
