# Dajngo Command to wait for DB to be ready

import time
from psycopg2 import OperationalError as Psycopg20pError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    #django command to wait for db
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database... ')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg20pError, OperationalError):
                self.stdout.write('Database is not available yet, wait for 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is Available!'))
