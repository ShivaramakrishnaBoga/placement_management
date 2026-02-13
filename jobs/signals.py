from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, JobDrive
from core.models import Notification

@receiver(post_save, sender=Application)
def create_application_notification(sender, instance, created, **kwargs):
    if not created:
        # Check if status changed? We don't have previous state easily here unless we track it
        # But we can assume an update to Application usually means status change or viewed
        # Actually viewed changes too.
        # Ideally, we check if status changed.
        # But for now, simple notification.
        pass

# Better approach for status change detection: pre_save or model clean
# Or just send notification in the ViewSet action update_status.
# The ViewSet is cleaner for "Business Logic" triggered by API.
# Signals are hidden magic.
# I will implement notification creation in ApplicationViewSet.update_status insteaf of signals.
