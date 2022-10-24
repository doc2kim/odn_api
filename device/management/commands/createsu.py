from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    help = "This command This command creates superuser"

    def handle(self, *args, **options):
        admin = User.objects.filter(username="admin")
        print('admin = ', admin)
        if not admin:
            User.objects.create_superuser(
                "admin", "admin@admin.com", "admin01323!")
            self.stdout.write(self.style.SUCCESS("Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser Exists"))
