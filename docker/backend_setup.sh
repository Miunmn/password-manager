#!/bin/sh


cd backend/password_management_api
python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8000 --settings=password_management_api.settings
