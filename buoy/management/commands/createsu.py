from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    
    help = "This command This command creates superuser"

    def handle(self, *args, **options):
        admin = User.objects.filter(email="doc2kim@naver.com")
        if not admin:
            User.objects.create_superuser("doc2kim","doc2kim@naver.com","Dkxltmxm22!")
            self.stdout.write(self.style.SUCCESS("Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser Exists"))