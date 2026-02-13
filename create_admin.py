import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_portal.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    user.role = 'ADMIN'
    user.save()
    print("Admin user created.")
from core.models import PlacementPolicy

if not PlacementPolicy.objects.filter(active_year=2024).exists():
    PlacementPolicy.objects.create(active_year=2024)
    print("Default Layout Policy created.")
else:
    print("Policy already exists.")
