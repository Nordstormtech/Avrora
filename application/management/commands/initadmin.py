from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os
class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:

            username = os.environ.get("ADMIN_USER", "admin")
            email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
            password = os.environ.get("ADMIN_PASSWORD", "password")
            print('Creating account for %s (%s)' % (username, email))
            user = User.objects.create_superuser(email=email, username=username, password=password)
            user.is_active = True
            user.is_admin = True
            user.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')