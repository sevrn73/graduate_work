import subprocess
import time

from django.core.management import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to pause execution until db is available"""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Database unavailable, waititng 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))

        p = subprocess.Popen(["python", "manage.py", "makemigrations"])
        p.wait()

        p = subprocess.Popen(["python", "manage.py", "migrate"])
        p.wait()

        p = subprocess.Popen(
            ["python", "manage.py", "createsuperuser", "--noinput", "--username=admin", "--email=admin@email.com"]
        )
        p.wait()

        subprocess.run(["gunicorn", "example.wsgi:application", "--workers=2", "--bind", "0.0.0.0:8000"])
