from django.core.management import call_command  # Ignore CPDBear
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('compilemessages', '-l', 'ru')
