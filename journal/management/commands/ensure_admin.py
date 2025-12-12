import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

class Command(BaseCommand):
    help = "Creates a default admin user if one does not exist"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('ADMIN_PASSWORD', 'adminpassword123')

        try:
            if not User.objects.filter(username=username).exists():
                self.stdout.write(f"Creating superuser: {username}")
                self.stdout.write(f"Email: {email}")
                
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Successfully created admin user: {username}'
                ))
                self.stdout.write(self.style.WARNING(
                    f'⚠ IMPORTANT: Save your admin credentials!'
                ))
                self.stdout.write(f'   Username: {username}')
                self.stdout.write(f'   Password: Check ADMIN_PASSWORD in environment variables')
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Admin user "{username}" already exists - skipping creation'
                ))
                
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(
                f'✗ Error creating admin user: {str(e)}'
            ))
            self.stdout.write(self.style.WARNING(
                'You may need to create an admin user manually using: python manage.py createsuperuser'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'✗ Unexpected error: {str(e)}'
            ))
