#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser if it doesn't exist
# Change 'admin', 'admin@example.com', 'adminpass123' with your own values
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='stevebay').exists() or User.objects.create_superuser('stevebay', 'bayonnestevekelly@gmail.com', 'jujub2b242*')" | python manage.py shell
