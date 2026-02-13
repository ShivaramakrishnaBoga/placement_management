from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from students.models import StudentProfile
from jobs.models import JobDrive, Application, Offer
from core.models import PlacementPolicy
from django.db.models import Count, Avg, Max
from django.db import models # Added import

class AdminAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_students = StudentProfile.objects.count()
        placed_students_count = StudentProfile.objects.filter(is_placed=True).count()
        placed_percentage = (placed_students_count / total_students * 100) if total_students > 0 else 0
        
        highest_package = StudentProfile.objects.aggregate(Max('highest_package'))['highest_package__max'] or 0
        avg_package = Offer.objects.filter(accepted=True).aggregate(Avg('ctc_offered'))['ctc_offered__avg'] or 0

        # Branch-wise stats
        branch_stats = StudentProfile.objects.values('branch').annotate(
            total=Count('id'),
            placed=Count('id', filter=models.Q(is_placed=True))
        )
        # Note: models.Q requires import
        
        # Company-wise hiring
        company_hiring = Offer.objects.filter(accepted=True).values('application__job__company_name').annotate(
            hires=Count('id')
        ).order_by('-hires')[:5]

        # Recent drives
        active_drives = JobDrive.objects.filter(status='OPEN').count()
        
        return Response({
            'total_students': total_students,
            'placed_students': placed_students_count,
            'placement_percentage': placed_percentage,
            'highest_package': highest_package,
            'average_package': avg_package,
            'branch_stats': branch_stats, # Need simpler serialization or list
            'top_companies': company_hiring,
            'active_drives': active_drives
        })
