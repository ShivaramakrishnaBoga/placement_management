from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.api_views import JobDriveViewSet, ApplicationViewSet
from students.api_views import StudentProfileViewSet
from analytics.api_views import AdminAnalyticsView

router = DefaultRouter()
router.register(r'jobs', JobDriveViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'students', StudentProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', AdminAnalyticsView.as_view(), name='analytics'),
]
