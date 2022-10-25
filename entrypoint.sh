#!/bin/sh

# python manage.py migrate --no-input

# python manage.py collectstatic --no-input

# python manage.py createsuperuser --username "odndev" --email "master@odn.us" --password "odn12006"
# echo "created superuser"


# DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput

# gunicorn django_project.wsgi:application --bind 0.0.0.0:8000