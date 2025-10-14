#!/bin/sh

python manage.py collectstatic
python manage.py migrate
python manage.py loaddata cities dev
python manage.py runserver 0.0.0.0:8000