#!/bin/sh

python manage.py collectstatic
python manage.py migrate
python manage.py loaddata cities dev
uvicorn template.asgi:application --host 0.0.0.0 --port 8000 --reload
