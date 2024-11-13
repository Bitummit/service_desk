#!/bin/sh

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python manage.py createsuperuser --noinput

python manage.py runserver 0.0.0.0:8000