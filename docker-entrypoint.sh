#!/bin/bash

# Migrate Database
python manage.py migrate --noinput

python manage.py createsu
# Run Gunicorn (WSGI Server)
gunicorn --bind 0.0.0.0:8000 config.wsgi:application