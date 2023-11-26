

from django.core import management
import os
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "Applies migrations and runs server"

   
    def handle(self, *args, **kwargs):
       management.call_command('makemigrations')
       management.call_command('migrate')
       management.call_command('generatedata')
       management.call_command('runserver')