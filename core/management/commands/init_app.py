
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Initializes the app: migrate and create default admin (admin/admin1234)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Applying migrations..."))
        call_command('migrate', interactive=False)
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.NOTICE("Creating default admin user..."))
            User.objects.create_superuser(username='admin', password='admin1234', email='admin@example.com')
        self.stdout.write(self.style.SUCCESS("Done. You can now run: python manage.py runserver"))
