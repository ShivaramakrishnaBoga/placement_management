from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import JobDrive, Application, Offer, ApplicationField, ApplicationResponse
from .serializers import JobDriveSerializer, ApplicationSerializer, OfferSerializer, ApplicationFieldSerializer
from .services import check_eligibility
from students.models import StudentProfile
from core.models import PlacementPolicy

class IsAdminOrOfficer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['ADMIN', 'OFFICER']

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'STUDENT'

class JobDriveViewSet(viewsets.ModelViewSet):
    queryset = JobDrive.objects.all()
    serializer_class = JobDriveSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'company_name', 'allowed_branches']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'STUDENT':
            # Students only see open/active jobs
            return JobDrive.objects.filter(status='OPEN')
        return JobDrive.objects.all()

    @action(detail=True, methods=['get'], permission_classes=[IsStudent])
    def check_eligibility(self, request, pk=None):
        job = self.get_object()
        student_profile = request.user.student_profile
        is_eligible, reasons = check_eligibility(student_profile, job)
        return Response({'eligible': is_eligible, 'reasons': reasons})

    @action(detail=True, methods=['post'], permission_classes=[IsStudent])
    def apply(self, request, pk=None):
        job = self.get_object()
        student_profile = request.user.student_profile
        
        # Check eligibility
        is_eligible, reasons = check_eligibility(student_profile, job)
        if not is_eligible:
            return Response({'error': 'Not Eligible', 'reasons': reasons}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check policy
        offer_count = Offer.objects.filter(application__student=request.user, accepted=True).count()
        policy = PlacementPolicy.objects.first() # Getting singleton (assuming created)
        if policy and offer_count >= policy.max_offers_per_student:
             # Check if upgrade logic applies (Dream/Super Dream vs existing offers)
             # Basic check for now
             if job.category == 'NORMAL' and student_profile.is_placed:
                  return Response({'error': 'Already placed and not eligible for further Normal offers'}, status=status.HTTP_400_BAD_REQUEST)
        
        application, created = Application.objects.get_or_create(job=job, student=request.user)
        if not created:
            return Response({'message': 'Already applied'}, status=status.HTTP_200_OK)
            
        return Response({'message': 'Application successful', 'application_id': application.id}, status=status.HTTP_201_CREATED)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'STUDENT':
            return Application.objects.filter(student=user)
        return Application.objects.all()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrOfficer])
    def update_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            return Response({'status': 'updated'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
