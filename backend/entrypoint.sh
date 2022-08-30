#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py test
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@mail.ru', '123')"| python manage.py shell
exec "$@"