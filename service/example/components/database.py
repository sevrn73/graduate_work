import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_NAME"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "OPTIONS": {"options": "-c search_path=public,content"},
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
