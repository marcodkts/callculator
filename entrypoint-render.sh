#!/bin/bash

# Run migrations
echo ">>> Run Migration"
python manage.py migrate -v 0

# Create superuser
echo "from django.conf import settings; from registration.models import User; User.objects.create_superuser(email=settings.DJANGO_SU_EMAIL, password=settings.DJANGO_SU_PASSWORD)" | python manage.py shell

# Start Django server
uvicorn core.asgi:application --host 0.0.0.0 --port 10000