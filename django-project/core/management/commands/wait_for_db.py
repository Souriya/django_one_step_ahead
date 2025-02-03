import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from psycopg import OperationalError as PsycopgError


class Command(BaseCommand):
    """django command to wait for DB to start before connecting to DB"""

    def handle(self, *args, **options):

        self.stdout.write('waiting for database ...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgError, OperationalError):
                self.stdout.write('database is not ready yet, wait for 1 sec ...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('database is ready ..'))
