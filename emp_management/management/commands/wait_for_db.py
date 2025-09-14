from django.core.management.base import BaseCommand
from django.db import connection
from time import sleep
import os

class Command(BaseCommand):
    help = 'Wait for database to be ready'

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                connection.ensure_connection()
                db_conn = True
                self.stdout.write(
                    self.style.SUCCESS('Database connection successful!')
                )
            except Exception as e:
                self.stdout.write(
                    f'Database unavailable, waiting 2 seconds... Error: {e}'
                )
                sleep(2)