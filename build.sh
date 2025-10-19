#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser if it doesn't exist (using environment variable for password)
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='stevebay').exists() or User.objects.create_superuser('stevebay', 'bayonnestevekelly@gmail.com', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell
fi
