from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def cleanup_unverified_users():
    expiry_time = timezone.now() - timedelta(days=1)
    users_to_delete = User.objects.filter(is_active=False, date_joined__lt=expiry_time)
    count = users_to_delete.count()
    users_to_delete.delete()
    print(f"Deleted {count} unverified users")
