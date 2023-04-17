#!/bin/sh

exec python manage.py collectstatic --no-input & python manage.py prepare_db_and_start