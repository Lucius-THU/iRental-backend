from django.core.management.base import BaseCommand, CommandError
from users.models import User

class Command(BaseCommand):
    help = 'create admin user'

    def handle(self, *args, **options):
        print('Enter email: ', end='')
        email = input()
        print('Enter password: ', end='')
        password = input()
        User.create(email=email, password=password, group='admin')
