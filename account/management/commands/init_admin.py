from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from account.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = "Will execute the admin"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="admin").exists():
            user = User.objects.create_superuser(
                username='admin', email='admin@gmail.com', password='admin')
            Profile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(
                " == == == == == == == == == == == == == =The admin created successfully != == == == == == == == == == == =="))
        else:
            self.stdout.write(self.style.NOTICE(
                "x x x x x x xx  xx  x xx  x x The admin already exists x x x xx  x x  xx x x   xx x  x xxx  "))
