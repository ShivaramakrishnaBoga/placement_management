from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.parsers import MultiPartParser, FormParser
from .models import StudentProfile
from .serializers import StudentProfileSerializer, AcademicDataSerializer
import openpyxl
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'STUDENT':
            # Only see own profile
            return StudentProfile.objects.filter(user=user)
        return StudentProfile.objects.all()

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser], permission_classes=[IsAdminUser])
    def upload_academic_excel(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            wb = openpyxl.load_workbook(file_obj)
            sheet = wb.active
            updated_count = 0
            errors = []
            
            # Assuming headers in first row: Roll Number, Name, Branch, CGPA, Backlogs, Year
            for row in sheet.iter_rows(min_row=2, values_only=True):
                roll_number, name, branch, cgpa, backlogs, year = row[:6]
                
                if not roll_number:
                    continue
                
                # Check for existing profile via roll number or create/find user
                # We assume User exists or we create them. For simplicity, assume User exists or link by Roll Number if stored in User
                # But StudentProfile has roll_number unique.
                
                try:
                    profile = StudentProfile.objects.get(roll_number=roll_number)
                    profile.cgpa = cgpa
                    profile.branch = branch
                    profile.active_backlogs = backlogs
                    profile.year = year
                    profile.academic_verified = True
                    profile.save()
                    updated_count += 1
                except StudentProfile.DoesNotExist:
                     errors.append(f"Profile for {roll_number} not found")
            
            return Response({'updated': updated_count, 'errors': errors})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
