import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Creates a default admin user if one does not exist"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('ADMIN_PASSWORD', 'adminpassword123')

        if not User.objects.filter(username=username).exists():
            self.stdout.write(f"Creating superuser: {username}")
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin user already exists'))
